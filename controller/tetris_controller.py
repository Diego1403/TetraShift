from __future__ import annotations

from pathlib import Path
from typing import Any, TYPE_CHECKING

import pygame
import numpy as np

from data.enums import Direction, ViewType
from data.config import (
    DEFAULT_BLINK_THRESHOLD, DEFAULT_BLINK_DURATION,
    DEFAULT_LEFT_GAZE_THRESHOLD, DEFAULT_RIGHT_GAZE_THRESHOLD,
    GAZE_COOLDOWN_FRAMES, BLINK_COOLDOWN_FRAMES, GAME_FPS,
)

if TYPE_CHECKING:
    from model.game_logic import GameLogic
    from view.game_display import GameDisplay

ButtonData = tuple[tuple[int, int], tuple[int, int]]

MODEL_PATH = Path("shape_predictor_68_face_landmarks.dat")


class TetrisController:
    """Handles keyboard, mouse, and eye-tracking input."""

    def __init__(self, gamelogic: GameLogic, view: GameDisplay) -> None:
        self.BLINK_THRESHOLD: float = DEFAULT_BLINK_THRESHOLD
        self.BLINK_TIME: float = DEFAULT_BLINK_DURATION
        self.LEFT_THRESHOLD: float = DEFAULT_LEFT_GAZE_THRESHOLD
        self.RIGHT_THRESHOLD: float = DEFAULT_RIGHT_GAZE_THRESHOLD

        self.gamelogic = gamelogic
        self.view = view
        self.view_type: ViewType = ViewType.START
        self.eye_detection: bool = self._init_gaze_tracking()
        self.blink_start_frame: int = 0
        self.gaze_cooldown: int = 0
        self.frame_count: int = 0

    def _init_gaze_tracking(self) -> bool:
        """Try to initialise webcam and dlib detectors. Return False on failure."""
        try:
            import cv2
            import dlib
        except ImportError:
            print("Eye tracking libraries not available — keyboard-only mode.")
            return False

        if not MODEL_PATH.exists():
            print(f"{MODEL_PATH} not found — eye tracking disabled.")
            return False

        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Webcam not available — keyboard-only mode.")
                return False
            self.detector = dlib.get_frontal_face_detector()
            self.predictor = dlib.shape_predictor(str(MODEL_PATH))
            self.cv2 = cv2
            self.cv_font = cv2.FONT_HERSHEY_SIMPLEX
        except Exception as exc:
            print(f"Eye tracking init failed ({exc}) — keyboard-only mode.")
            return False
        return True

    def cleanup(self) -> None:
        """Release the camera if it was opened."""
        if self.eye_detection and hasattr(self, "cap"):
            self.cap.release()

    def handle_event(self) -> None:
        """Process all pending input events for one frame."""
        self.frame_count += 1

        if self.eye_detection and self.gaze_cooldown <= 0:
            direction = self._check_gaze_direction()
            if direction != Direction.NONE:
                self.gamelogic.set_direction(direction)
                self.gaze_cooldown = GAZE_COOLDOWN_FRAMES
        if self.gaze_cooldown > 0:
            self.gaze_cooldown -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gamelogic.request_exit()
                self.cleanup()
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.gamelogic.set_direction(Direction.LEFT)
                if event.key == pygame.K_RIGHT:
                    self.gamelogic.set_direction(Direction.RIGHT)
                if event.key == pygame.K_UP:
                    self.gamelogic.set_direction(Direction.ROTATE)
                if event.key == pygame.K_DOWN:
                    self.gamelogic.set_direction(Direction.DOWN)

            self.view_type = self.view.get_view_type()
            if self.view_type == ViewType.START:
                self.check_button_click(
                    event, self.view.get_start_button_data(), "startButton"
                )
            if self.view_type == ViewType.GAME:
                self.check_button_click(
                    event, self.view.get_pause_button_data(), "pauseButton"
                )
            if self.view_type == ViewType.PAUSE:
                self.check_button_click(
                    event, self.view.get_continue_button_data(), "continueButton"
                )

            if self.view_type == ViewType.GAMEOVER or self.view_type == ViewType.PAUSE:
                self.check_button_click(
                    event, self.view.get_exit_button_data(), "exitButton"
                )

            if self.view_type == ViewType.GAMEOVER:
                self.check_button_click(
                    event, self.view.get_try_again_button_data(), "tryAgainButton"
                )

    def check_button_click(
        self, event: pygame.event.Event, button: ButtonData, tipo: str
    ) -> None:
        """Check if *event* is a click inside *button* and dispatch the action."""
        button_coords = button[0]
        button_rect = button[1]
        button_x = button_coords[0]
        button_y = button_coords[1]
        button_width = button_rect[0]
        button_height = button_rect[1]
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (
                button_x <= mouse_pos[0] <= button_x + button_width
                and button_y <= mouse_pos[1] <= button_y + button_height
            ):
                if tipo == "startButton":
                    self.gamelogic.change_view_type(
                        ViewType.GAME, self.gamelogic.light_mode
                    )
                elif tipo == "pauseButton":
                    self.gamelogic.change_view_type(
                        ViewType.PAUSE, self.gamelogic.light_mode
                    )
                    self.gamelogic.set_paused(True)
                elif tipo == "continueButton":
                    self.gamelogic.set_paused(False)
                    self.gamelogic.change_view_type(
                        ViewType.GAME, self.gamelogic.light_mode
                    )
                elif tipo == "exitButton":
                    self.gamelogic.request_exit()
                    self.cleanup()
                    pygame.display.quit()
                    quit()
                elif tipo == "tryAgainButton":
                    self.gamelogic.exit_game = False
                    self.gamelogic.set_paused(False)
                    self.gamelogic.reset_game()
                    self.gamelogic.change_view_type(
                        ViewType.GAME, self.gamelogic.light_mode
                    )

    def _check_gaze_direction(self) -> Direction:
        """Read one camera frame and return the detected gaze direction."""
        cv2 = self.cv2
        ret, frame = self.cap.read()
        if not ret or frame is None:
            return Direction.NONE

        self.frame = frame
        self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(self.gray)
        d = Direction.NONE

        for face in faces:
            landmarks = self.predictor(self.gray, face)
            left_eye_ratio = self._get_blinking_ratio(
                [36, 37, 38, 39, 40, 41], landmarks
            )
            right_eye_ratio = self._get_blinking_ratio(
                [42, 43, 44, 45, 46, 47], landmarks
            )

            if (right_eye_ratio + left_eye_ratio) / 2 > self.BLINK_THRESHOLD:
                if self.blink_start_frame == 0:
                    self.blink_start_frame = self.frame_count
                else:
                    elapsed = self.frame_count - self.blink_start_frame
                    if elapsed >= self.BLINK_TIME * GAME_FPS:
                        d = Direction.ROTATE
                        self.gaze_cooldown = BLINK_COOLDOWN_FRAMES
                        cv2.imshow("Frame", frame)
                        return d
            else:
                self.blink_start_frame = 0

            gaze_ratio_left = self._get_gaze_ratio(
                [36, 37, 38, 39, 40, 41], landmarks
            )
            gaze_ratio_right = self._get_gaze_ratio(
                [42, 43, 44, 45, 46, 47], landmarks
            )
            gaze_ratio = (gaze_ratio_right + gaze_ratio_left) / 2

            if gaze_ratio <= self.RIGHT_THRESHOLD:
                cv2.putText(frame, "RIGHT", (50, 100), self.cv_font, 2, (0, 0, 255), 3)
                d = Direction.RIGHT
                cv2.imshow("Frame", frame)
                return d
            elif self.RIGHT_THRESHOLD < gaze_ratio < self.LEFT_THRESHOLD:
                cv2.putText(frame, "CENTER", (50, 100), self.cv_font, 2, (0, 0, 255), 3)
                cv2.imshow("Frame", frame)
                d = Direction.NONE
                break
            else:
                cv2.putText(frame, "LEFT", (50, 100), self.cv_font, 2, (0, 0, 255), 3)
                d = Direction.LEFT
                cv2.imshow("Frame", frame)
                return d

        cv2.imshow("Frame", frame)
        return d

    def _get_gaze_ratio(self, eye_points: list[int], facial_landmarks: Any) -> float:
        """Calculate the left/right white-pixel ratio for gaze detection."""
        cv2 = self.cv2
        left_eye_region = np.array(
            [
                (
                    facial_landmarks.part(eye_points[i]).x,
                    facial_landmarks.part(eye_points[i]).y,
                )
                for i in range(6)
            ],
            np.int32,
        )
        height, width, _ = self.frame.shape
        mask = np.zeros((height, width), np.uint8)
        cv2.polylines(mask, [left_eye_region], True, 255, 2)
        cv2.fillPoly(mask, [left_eye_region], 255)
        eye = cv2.bitwise_and(self.gray, self.gray, mask=mask)
        min_x = np.min(left_eye_region[:, 0])
        max_x = np.max(left_eye_region[:, 0])
        min_y = np.min(left_eye_region[:, 1])
        max_y = np.max(left_eye_region[:, 1])
        gray_eye = eye[min_y:max_y, min_x:max_x]
        _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
        height, width = threshold_eye.shape

        left_side_threshold = threshold_eye[0:height, 0 : int(width / 2)]
        left_side_white = cv2.countNonZero(left_side_threshold)

        right_side_threshold = threshold_eye[0:height, int(width / 2) : width]
        right_side_white = cv2.countNonZero(right_side_threshold)

        if left_side_white == 0:
            return 1.0
        elif right_side_white == 0:
            return 5.0
        else:
            return left_side_white / right_side_white

    @staticmethod
    def _midpoint(p1: Any, p2: Any) -> tuple[int, int]:
        return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

    @staticmethod
    def _hypot(x: int | float, y: int | float) -> int:
        return int(np.sqrt(x * x + y * y))

    def _get_blinking_ratio(self, eye_points: list[int], facial_landmarks: Any) -> float:
        """Calculate the horizontal/vertical line ratio to detect blinks."""
        cv2 = self.cv2
        left_point = (
            facial_landmarks.part(eye_points[0]).x,
            facial_landmarks.part(eye_points[0]).y,
        )
        right_point = (
            facial_landmarks.part(eye_points[3]).x,
            facial_landmarks.part(eye_points[3]).y,
        )
        center_top = self._midpoint(
            facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2])
        )
        center_bottom = self._midpoint(
            facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4])
        )
        cv2.line(self.frame, left_point, right_point, (0, 255, 0), 2)
        cv2.line(self.frame, center_top, center_bottom, (0, 255, 0), 2)
        hor_line_length = self._hypot(
            (left_point[0] - right_point[0]), (left_point[1] - right_point[1])
        )
        ver_line_length = self._hypot(
            (center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1])
        )
        ratio = hor_line_length / ver_line_length
        return ratio

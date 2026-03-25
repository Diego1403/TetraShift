import time

import pygame
import cv2
import numpy as np
import dlib

from data.enums import Direction, ViewType


class TetrisController:
    def __init__(self, gamelogic, view):
        self.BLINK_THRESHOLD = 6
        self.BLINK_TIME = 1
        self.LEFT_THRESHOLD = 3
        self.RIGHT_THRESHOLD = 0.4

        self.gamelogic = gamelogic
        self.view = view
        self.view_type = ViewType.START
        self.eye_detection = True

        if self.eye_detection:
            self.init_gaze_tracking()
        self.blink_start_time = 0

    def init_gaze_tracking(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def handle_event(self):
        if self.eye_detection:
            self.gamelogic.set_direction(self.check_gaze_direction())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gamelogic.request_exit()
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

    def check_button_click(self, event, button, tipo):
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
                    pygame.display.quit()
                    quit()
                elif tipo == "tryAgainButton":
                    self.gamelogic.exit_game = False
                    self.gamelogic.set_paused(False)
                    self.gamelogic.reset_game()
                    self.gamelogic.change_view_type(
                        ViewType.GAME, self.gamelogic.light_mode
                    )

    def check_gaze_direction(self):
        self._, self.frame = self.cap.read()
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.faces = self.detector(self.gray)
        d = Direction.NONE
        for face in self.faces:
            landmarks = self.predictor(self.gray, face)
            left_eye_ratio = self.get_blinking_ratio(
                [36, 37, 38, 39, 40, 41], landmarks
            )
            right_eye_ratio = self.get_blinking_ratio(
                [42, 43, 44, 45, 46, 47], landmarks
            )

            if (right_eye_ratio + left_eye_ratio) / 2 > self.BLINK_THRESHOLD:
                if self.blink_start_time == 0:
                    self.blink_start_time = time.time()
                else:
                    if time.time() - self.blink_start_time >= self.BLINK_TIME:
                        d = Direction.ROTATE
                        time.sleep(1)
                        return d
            else:
                self.blink_start_time = 0

            gaze_ratio_left_eye = self.get_gaze_ratio(
                [36, 37, 38, 39, 40, 41], landmarks
            )
            gaze_ratio_right_eye = self.get_gaze_ratio(
                [42, 43, 44, 45, 46, 47], landmarks
            )
            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
            if gaze_ratio <= self.RIGHT_THRESHOLD:
                cv2.putText(
                    self.frame, "RIGHT", (50, 100), self.font, 2, (0, 0, 255), 3
                )
                d = Direction.RIGHT
                cv2.imshow("Frame", self.frame)
                time.sleep(0.2)
                return d
            elif self.RIGHT_THRESHOLD < gaze_ratio < self.LEFT_THRESHOLD:
                cv2.putText(
                    self.frame, "CENTER", (50, 100), self.font, 2, (0, 0, 255), 3
                )
                cv2.imshow("Frame", self.frame)
                d = Direction.NONE
                break
            else:
                cv2.putText(
                    self.frame, "LEFT", (50, 100), self.font, 2, (0, 0, 255), 3
                )
                d = Direction.LEFT
                cv2.imshow("Frame", self.frame)
                time.sleep(0.2)
                return d

        cv2.imshow("Frame", self.frame)
        return d

    def get_gaze_ratio(self, eye_points, facial_landmarks):
        left_eye_region = np.array(
            [
                (
                    facial_landmarks.part(eye_points[0]).x,
                    facial_landmarks.part(eye_points[0]).y,
                ),
                (
                    facial_landmarks.part(eye_points[1]).x,
                    facial_landmarks.part(eye_points[1]).y,
                ),
                (
                    facial_landmarks.part(eye_points[2]).x,
                    facial_landmarks.part(eye_points[2]).y,
                ),
                (
                    facial_landmarks.part(eye_points[3]).x,
                    facial_landmarks.part(eye_points[3]).y,
                ),
                (
                    facial_landmarks.part(eye_points[4]).x,
                    facial_landmarks.part(eye_points[4]).y,
                ),
                (
                    facial_landmarks.part(eye_points[5]).x,
                    facial_landmarks.part(eye_points[5]).y,
                ),
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
            gaze_ratio = 1
        elif right_side_white == 0:
            gaze_ratio = 5
        else:
            gaze_ratio = left_side_white / right_side_white
        return gaze_ratio

    def midpoint(self, p1, p2):
        return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

    def hypot(self, x, y):
        return int(np.sqrt(x * x + y * y))

    def get_blinking_ratio(self, eye_points, facial_landmarks):
        left_point = (
            facial_landmarks.part(eye_points[0]).x,
            facial_landmarks.part(eye_points[0]).y,
        )
        right_point = (
            facial_landmarks.part(eye_points[3]).x,
            facial_landmarks.part(eye_points[3]).y,
        )
        center_top = self.midpoint(
            facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2])
        )
        center_bottom = self.midpoint(
            facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4])
        )
        hor_line = cv2.line(self.frame, left_point, right_point, (0, 255, 0), 2)
        ver_line = cv2.line(self.frame, center_top, center_bottom, (0, 255, 0), 2)
        hor_line_length = self.hypot(
            (left_point[0] - right_point[0]), (left_point[1] - right_point[1])
        )
        ver_line_length = self.hypot(
            (center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1])
        )
        ratio = hor_line_length / ver_line_length
        return ratio

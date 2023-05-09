import pygame
import cv2, sys
import numpy as np

# used to detect faces
import dlib
from data.constants import Direction, ViewType


class TetrisController:
    def __init__(self, gamelogic, view):
        self.gamelogic = gamelogic
        self.view = view
        self.eye_detection = False
        # gaze tracking init
        if self.eye_detection:
            self.init_gaze_tracking()

    def init_gaze_tracking(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = dlib.get_frontal_face_detector()
        # used to detect facial landmarks
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def handle_event(self):
        # handle gaze input

        # we use gray scale to save computation power

        if self.eye_detection:
            self.gamelogic.dir = self.check_gaze_direction()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gamelogic.gameOver = True
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.gamelogic.dir = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.gamelogic.dir = Direction.RIGHT
                if event.key == pygame.K_UP:
                    self.gamelogic.dir = Direction.ROTATE
                if event.key == pygame.K_DOWN:
                    # move shape down and force move events
                    self.gamelogic.dir = Direction.DOWN
            self.check_button(event, self.view.get_StartButtonData(), "startButton")
            self.check_button(event, self.view.get_PauseButtonData(), "pauseButton")
            self.check_button(
                event, self.view.get_ContinueButtonData(), "continueButton"
            )
            self.check_button(event, self.view.get_ExitButtonData(), "exitButton")

    def check_button(self, event, Button, tipo):
        ButtonCoords = Button[0]
        ButtonRect = Button[1]
        button_x = ButtonCoords[0]
        button_y = ButtonCoords[1]
        button_width = ButtonRect[0]
        button_height = ButtonRect[1]
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (
                button_x <= mouse_pos[0] <= button_x + button_width
                and button_y <= mouse_pos[1] <= button_y + button_height
            ):
                if tipo == "startButton":
                    self.gamelogic.changeViewType(
                        ViewType.GAME, self.gamelogic.lightMode
                    )
                elif tipo == "pauseButton":
                    self.gamelogic.changeViewType(
                        ViewType.PAUSE, self.gamelogic.lightMode
                    )
                    self.gamelogic.pause = True
                elif tipo == "continueButton":
                    self.gamelogic.pause = False
                    self.gamelogic.changeViewType(
                        ViewType.GAME, self.gamelogic.lightMode
                    )
                elif tipo == "exitButton":
                    self.gamelogic.gameOver = True
                    pygame.display.quit()
                    quit()

    def check_gaze_direction(self):
        self._, self.frame = self.cap.read()
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.faces = self.detector(self.gray)
        d = Direction.DOWN
        for face in self.faces:
            landmarks = self.predictor(self.gray, face)
            # detect blinking
            # the numbers are the index of the facial landmarks
            left_eye_ratio = self.get_blinking_ratio(
                [36, 37, 38, 39, 40, 41], landmarks
            )
            right_eye_ratio = self.get_blinking_ratio(
                [42, 43, 44, 45, 46, 47], landmarks
            )

            mouth_ratio = self.get_mouth_ratio([61, 62, 63, 64, 65, 66, 67], landmarks)

            rotate = False
            if right_eye_ratio + left_eye_ratio / 2 > 6:
                d = Direction.ROTATE
                break

            # gaze detection
            # the numbers are the index of the facial landmarks , we want to get all of the points in the left eye and draw a polygon around it

            # Gaze detection
            gaze_ratio_left_eye = self.get_gaze_ratio(
                [36, 37, 38, 39, 40, 41], landmarks
            )
            gaze_ratio_right_eye = self.get_gaze_ratio(
                [42, 43, 44, 45, 46, 47], landmarks
            )
            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
            new_frame = np.zeros((500, 500, 3), np.uint8)
            print(gaze_ratio)
            if gaze_ratio <= 1:
                cv2.putText(
                    self.frame, "RIGHT", (50, 100), self.font, 2, (0, 0, 255), 3
                )
                d = Direction.RIGHT
                break
                new_frame[:] = (0, 0, 255)
            elif 1 < gaze_ratio < 2:
                cv2.putText(
                    self.frame, "CENTER", (50, 100), self.font, 2, (0, 0, 255), 3
                )
                d = Direction.DOWN
            else:
                new_frame[:] = (255, 0, 0)
                cv2.putText(self.frame, "LEFT", (50, 100), self.font, 2, (0, 0, 255), 3)
                d = Direction.LEFT
                break

        cv2.imshow("Frame", self.frame)
        return d

    def get_mouth_ratio(self, mouth_points, facial_landmarks):
        mouth_region = np.array(
            [
                (
                    facial_landmarks.part(mouth_points[0]).x,
                    facial_landmarks.part(mouth_points[0]).y,
                ),
                (
                    facial_landmarks.part(mouth_points[1]).x,
                    facial_landmarks.part(mouth_points[1]).y,
                ),
                (
                    facial_landmarks.part(mouth_points[2]).x,
                    facial_landmarks.part(mouth_points[2]).y,
                ),
                (
                    facial_landmarks.part(mouth_points[3]).x,
                    facial_landmarks.part(mouth_points[3]).y,
                ),
                (
                    facial_landmarks.part(mouth_points[4]).x,
                    facial_landmarks.part(mouth_points[4]).y,
                ),
                (
                    facial_landmarks.part(mouth_points[5]).x,
                    facial_landmarks.part(mouth_points[5]).y,
                ),
                (
                    facial_landmarks.part(mouth_points[6]).x,
                    facial_landmarks.part(mouth_points[6]).y,
                ),
            ],
            np.int32,
        )

        # we draw a polygon around the left eye
        height, width, _ = self.frame.shape
        mask = np.zeros((height, width), np.uint8)
        cv2.polylines(mask, [mouth_region], True, 255, 2)
        cv2.fillPoly(mask, [mouth_region], 255)
        eye = cv2.bitwise_and(self.gray, self.gray, mask=mask)
        # we get the min and max values of the x and y coordinates
        min_x = np.min(mouth_region[:, 0])
        max_x = np.max(mouth_region[:, 0])
        min_y = np.min(mouth_region[:, 1])
        max_y = np.max(mouth_region[:, 1])
        # we get the gray eye

    # we divide the left side white pixels by the right side white pixels
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
        # we draw a polygon around the left eye
        height, width, _ = self.frame.shape
        mask = np.zeros((height, width), np.uint8)
        cv2.polylines(mask, [left_eye_region], True, 255, 2)
        cv2.fillPoly(mask, [left_eye_region], 255)
        eye = cv2.bitwise_and(self.gray, self.gray, mask=mask)
        # we get the min and max values of the x and y coordinates
        min_x = np.min(left_eye_region[:, 0])
        max_x = np.max(left_eye_region[:, 0])
        min_y = np.min(left_eye_region[:, 1])
        max_y = np.max(left_eye_region[:, 1])
        # we get the gray eye
        gray_eye = eye[min_y:max_y, min_x:max_x]
        # we get the white pixels
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

    # calculates the midpoint between two points
    def midpoint(self, p1, p2):
        return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

    # calculates the distance between two points
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
        hor_line_lenght = self.hypot(
            (left_point[0] - right_point[0]), (left_point[1] - right_point[1])
        )
        ver_line_lenght = self.hypot(
            (center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1])
        )
        ratio = hor_line_lenght / ver_line_lenght
        return ratio

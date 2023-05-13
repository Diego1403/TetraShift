import time
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
        self.viewType = ViewType.START
        self.eye_detection = True
        self.EYE_AR_THRESH = 0.19
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

            self.viewType = self.view.get_ViewType()
            if self.viewType == ViewType.START:
                self.check_button(event, self.view.get_StartButtonData(), "startButton")
            if self.viewType == ViewType.GAME:
                self.check_button(event, self.view.get_PauseButtonData(), "pauseButton")
            if self.viewType == ViewType.PAUSE:
                self.check_button(
                    event, self.view.get_ContinueButtonData(), "continueButton"
                )

            if self.viewType == ViewType.GAMEOVER or self.view == ViewType.PAUSE:
                self.check_button(event, self.view.get_ExitButtonData(), "exitButton")

            if self.viewType == ViewType.GAMEOVER:
                self.check_button(
                    event, self.view.get_TryAgainButtonData(), "tryAgainButton"
                )

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
                elif tipo == "tryAgainButton":
                    self.gamelogic.gameOver = False
                    self.gamelogic.pause = False
                    self.gamelogic.reset_game()

                    self.gamelogic.changeViewType(
                        ViewType.GAME, self.gamelogic.lightMode
                    )

    def check_gaze_direction(self):
        self._, self.frame = self.cap.read()
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.faces = self.detector(self.gray)
        d = Direction.NONE

        # Counters for closed eyes
        self.right_eye_close_counter = 0
        self.left_eye_close_counter = 0

        # Threshold for eye closure in frames
        eye_close_threshold = 1  # Set this according to your needs

        for face in self.faces:
            landmarks = self.predictor(self.gray, face)
            left_eye_ear = self.get_ear([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ear = self.get_ear([42, 43, 44, 45, 46, 47], landmarks)

            # Average EAR
            ear = (left_eye_ear + right_eye_ear) / 2.0

            print("left eye EAR: ", left_eye_ear)
            print("right eye EAR: ", right_eye_ear)
            d = Direction.NONE
            # consider that the eye is blink if the ear is less than threshold
            if ear < self.EYE_AR_THRESH:
                self.left_eye_close_counter += 1
                self.right_eye_close_counter += 1
                if (
                    self.right_eye_close_counter >= eye_close_threshold
                    and self.left_eye_close_counter >= eye_close_threshold
                ):
                    d = Direction.ROTATE
                    # Reset counters
                    self.right_eye_close_counter = 0
                    self.left_eye_close_counter = 0
                    time.sleep(0.05)
                    return d
                break

            # right eye is closed
            elif right_eye_ear < self.EYE_AR_THRESH:
                self.right_eye_close_counter += 1
                if self.right_eye_close_counter >= eye_close_threshold:
                    d = Direction.RIGHT
                    print("right eye close")
                    # Reset counter
                    self.right_eye_close_counter = 0
                    time.sleep(0.05)
                    return d
                break
            # left eye is closed
            elif left_eye_ear < self.EYE_AR_THRESH :
                self.left_eye_close_counter += 1
                if self.left_eye_close_counter >= eye_close_threshold:
                    d = Direction.LEFT
                    print("left eye close")
                    # Reset counter
                    self.left_eye_close_counter = 0
                    time.sleep(0.05)
                    return d

                # gaze detection
                # the numbers are the index of the facial landmarks , we want to get all of the points in the left eye and draw a polygon around it

                # Gaze detection
                # gaze_ratio_left_eye = self.get_gaze_ratio(
                #     [36, 37, 38, 39, 40, 41], landmarks
                # )
                # gaze_ratio_right_eye = self.get_gaze_ratio(
                #     [42, 43, 44, 45, 46, 47], landmarks
                # )
                # gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2
                # new_frame = np.zeros((500, 500, 3), np.uint8)
                # print(gaze_ratio)
                # if gaze_ratio <= 1:
                #     cv2.putText(
                #         self.frame, "RIGHT", (50, 100), self.font, 2, (0, 0, 255), 3
                #     )
                #     print("gaze right")
                #     d = Direction.RIGHT
                #     break
                #     new_frame[:] = (0, 0, 255)
                # elif 1 < gaze_ratio < 2:
                #     cv2.putText(
                #         self.frame, "CENTER", (50, 100), self.font, 2, (0, 0, 255), 3
                #     )
                #     print("gaze center")
                #     d = Direction.NONE
                # else:
                #     new_frame[:] = (255, 0, 0)
                #     cv2.putText(self.frame, "LEFT", (50, 100), self.font, 2, (0, 0, 255), 3)
                #     d = Direction.LEFT
                #     print("gaze left")
                #     break

            #cv2.imshow("Frame", self.frame)
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

    # calculates the eye aspect ratio (EAR)
    def get_ear(self, eye_points, facial_landmarks):
        # compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
        A = np.linalg.norm(
            np.array(
                (
                    facial_landmarks.part(eye_points[1]).x,
                    facial_landmarks.part(eye_points[1]).y,
                )
            )
            - np.array(
                (
                    facial_landmarks.part(eye_points[5]).x,
                    facial_landmarks.part(eye_points[5]).y,
                )
            )
        )
        B = np.linalg.norm(
            np.array(
                (
                    facial_landmarks.part(eye_points[2]).x,
                    facial_landmarks.part(eye_points[2]).y,
                )
            )
            - np.array(
                (
                    facial_landmarks.part(eye_points[4]).x,
                    facial_landmarks.part(eye_points[4]).y,
                )
            )
        )

        # compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
        C = np.linalg.norm(
            np.array(
                (
                    facial_landmarks.part(eye_points[0]).x,
                    facial_landmarks.part(eye_points[0]).y,
                )
            )
            - np.array(
                (
                    facial_landmarks.part(eye_points[3]).x,
                    facial_landmarks.part(eye_points[3]).y,
                )
            )
        )

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        return ear

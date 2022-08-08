import cv2
import numpy as np
import os

def Trunk_Score(x):
    vector_a = np.array([0, 0, 1])
    vector_b = x[0] - x[8]
    angle = 180-(
        np.arccos(vector_a.dot(vector_b)/(np.linalg.norm(vector_a) * np.linalg.norm(vector_b))))*360/2/np.pi
    # print("trunk_angle:",angle)
    if angle <= 8 :
        score = 1
    elif 8<angle<=45:
        score = 2
    elif 45<angle<60:
        score =3
    else:
        score =4
    return score

def Neck_Score(x):
    vector_a = np.array([0, 0, 1])
    vector_b = x[8] - x[9]
    angle = 180 - (
        np.arccos(vector_a.dot(vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b)))) * 360 / 2 / np.pi
    # print("Neck_angle:", angle)
    if 20 < angle <= 60:
        score = 1
    elif angle > 60:
        score = 2
    else:
        score = 0
    return score

def Legs_Score(x):
    vector_a = np.array([0, 0, 1])
    vector_b = x[2] - x[1]
    vector_c = x[5] - x[4]
    angle1 = 180 - (
        np.arccos(vector_a.dot(vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b)))) * 360 / 2 / np.pi
    angle2 = 180 - (
        np.arccos(vector_a.dot(vector_c) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_c)))) * 360 / 2 / np.pi
    # print(f"legs_angle1/legs_angle1:{angle1},{angle2}")
    if abs(angle1) >= abs(angle2):
        angle = angle1
    else:
        angle = angle2
    if 30 < angle <= 60:   #30,60
        score1 = 1
    elif angle > 60:
        score1 = 2
    else:
        score1 = 0
    if abs(angle1-angle2)>=20:
        return score1+2
    else:
        return score1+1

def Upper_arms_Score(x):
    vector_a = np.array([0, 0, -1])
    vector_b = x[14] - x[15]
    angle = 180 - (
        np.arccos(vector_a.dot(vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b)))) * 360 / 2 / np.pi
    # print("Upper_arms_angle:", angle)
    if 6 < angle < 30:  #6-20
        score = 1
    elif 30 <= angle <60:   #20-45
        score = 2
    elif 60 <= angle <= 90: #45-90
        score = 3
    elif angle > 90:        #>90
        score = 4
    else:
        score = 0
    return score

def Lower_arms_Score(x):
    vector_a = np.array([0, 0, -1])
    vector_b = x[15] - x[16]
    angle = 180 - (
        np.arccos(vector_a.dot(vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b)))) * 360 / 2 / np.pi
    # print("Lower_arms_angle:", angle)
    if 60 <= angle <= 100:
        score = 1
    elif 6 < angle <60 or angle >100:  #6,60,100
        score = 2
    else:
        score = 0
    return score

def reba_eval(b):
    wrist_score = 1
    level_1,level_2, level_3,level_4 = 0,0,0,0
    reba_text = []
    action_levels= []
    for i in range(dimension[0]):
        print(f"Frame：{i}")
        trunk_score = Trunk_Score(b[i])
        print("trunk_score=",trunk_score)
        neck_score = Neck_Score(b[i])
        print("neck_score=", neck_score)
        legs_score = Legs_Score(b[i])
        print("legs_score=", legs_score)
        upper_arms_score = Upper_arms_Score(b[i])
        print("upper_arms_score=", upper_arms_score)
        lower_arms_score = Lower_arms_Score(b[i])
        print("lower_arms_score=", lower_arms_score)
        reba_score = trunk_score + neck_score + legs_score + upper_arms_score + lower_arms_score + wrist_score
        if reba_score == 1:
            Action_level = 0
        elif 2 <= reba_score <= 3:
            Action_level = 1
            level_1 += 1
        elif 4 <= reba_score <= 7:
            Action_level = 2
            level_2 += 1
        elif 8 <= reba_score <= 10:
            Action_level = 3
            level_3 += 1
        elif 11 <= reba_score <= 15:
            Action_level = 4
            level_4 += 1
        ori_text = "reba_score:" + str(reba_score) +" "+ "action_level:" + str(Action_level)
        action_levels.append(Action_level)
        reba_text.append(ori_text)
        print(f'reba_score and action_level = {reba_score},{Action_level}')

    print("action_levels=",action_levels)
    return reba_text

fo = np.load('outputfile.npy',encoding = "latin1")
np.set_printoptions(threshold=np.inf)
np.set_printoptions(suppress=True)
b = np.around(fo,5)
print("b.shape=",b.shape)
dimension = list(np.array(b).shape)


def reba():
    oir_path = 'output.mp4'
    dir_path = 'reba.mp4'
    cap = cv2.VideoCapture(oir_path)
    out_file =  os.path.abspath(dir_path)
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames_num = cap.get(7)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)
    video_writer = cv2.VideoWriter(out_file, fourcc, fps, frame_size)
    text = reba_eval(b)
    # print("frames_num", frames_num)
    # print("len(text)", len(text))
    if len(text) > int(frames_num):
        difference = len(text) - int(frames_num)
        for k in range(difference):
            text.pop(-1)
    assert len(text) == int(frames_num)
    num = 0
    ind = 0
    while ind < frames_num:
        ind += 1
        ret, img = cap.read()
        word = text[num]
        cv2.putText(img, word, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        if num < (len(text)-1):
            num+=1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        video_writer.write(img)
    cap.release()

if name =="__main__":
    reba()








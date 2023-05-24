def normalize_flow_datas(boxes_ID,frame_count):
    data_frame = []

    if len(boxes_ID) > 0:
        data_frame.append(boxes_ID[0][4])
        data_frame.append(boxes_ID[0][1])
        data_frame.append(frame_count)
        #print(data_frame)
    
    return data_frame

def flow_speed_calculus(flow_frame):
    speed = 0 
    if len(flow_frame) > 29 and flow_frame[len(flow_frame)-1][0] == flow_frame[len(flow_frame)-11][0]: 
        speed = flow_frame[len(flow_frame)-31][1] - flow_frame[len(flow_frame)-1][1]
        # Probablement plus simple de mettre un Dataframe pour calculer la vitesse moyenne sur la periode d'apparition. 

    elif len(flow_frame) > 29 and flow_frame[len(flow_frame)-1][0] != flow_frame[len(flow_frame)-11][0]:
        # Avant de clear:
        # Faire la moyenne des vitesses observées en pps (pixel par seconde) pour l'objet numéro n. 
        # Renseigner un tableau. 
        flow_frame.clear()

    return speed

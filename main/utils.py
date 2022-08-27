import numpy as np
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow import keras
import os,csv,pickle,random


img_height = 224
img_width = 224
#Constant Image Height and width

def crop_recommend(n,p,k,ph,rf,temp,hum):
    """
    Take the input parameters and recommend a suitable crop for the user.

    Parameters
    ----------
        n - Nitrogen : str
        p - phosphurus : str
        k - potassium : str
        ph - pH value : str
        rf - Rainfall : str
        temp - Temperature : str
        hum - Humidity : str

    Example
    -------
        n = p = k = '78',
        ph = '7',
        rf = '200',
        temp = '30',
        hum = '34'

    Returns
    ------
        context - JSON context for html : dictionary
    """

    DIF1 = random.randint(15,40)
    DIF = random.randint(5,10)
    DIF2 = random.randint(3,6)

    tdf = pd.read_csv(r'static\CropDesc.csv')
    #temp,hum = get_params(c)
    file = r'static\Random Forest Classifier.pkl'
    model = pickle.load(open(file, 'rb'))

    l = [int(n),int(p),int(k),int(temp),int(hum),int(ph),int(rf)]
    crop = model.predict([l])
    fin = crop[0]

    num = tdf[tdf['label']==fin]['discription'].index[0]
    tstr = tdf['discription'][num]

    if l[0]>10 and l[1]>10 and l[2]>10 and l[5]>1 and l[5]<14 and l[3]>6 and l[4]>6 and l[6]>40:
        d = f'{fin.upper()} requires land with {l[0]-DIF} mg/kg to {l[0]+DIF} mg/kg Nitrogen and {l[1]-DIF} mg/kg to {l[1]+DIF} mg/kg Phosphorus as well as {l[2]-DIF} mg/kg to {l[2]+DIF} mg/kg Potassium. Moreover,Temperature between {l[3]-DIF2}℃ and {l[3]+DIF2}℃ is sufficient to cultivate it if {l[4]-DIF}% to {l[4]+DIF}%  Humidity is maintained.{fin.upper()} grow well in area having {l[6]-DIF1}mm to {l[6]+DIF1} Rainfall.Additionally, {l[5]-1} to {l[5]+1} ph scale is ideal for {fin.upper()}.'
    else:
        d = f'{fin.upper()} requires land with {l[0]-1} mg/kg to {l[0]+DIF} mg/kg Nitrogen and {l[1]-3} mg/kg to {l[1]+DIF} mg/kg Phosphorus as well as {l[2]-2} mg/kg to {l[2]+DIF} mg/kg Potasssium. Moreover,Temperature between {l[3]}℃ and {l[3]+DIF2}℃ is sufficient to cultivate it if {l[4]+1}% to {l[4]+DIF}%  Humidity is maintained.{fin.upper()} grow well in area having {l[6]+10}mm to {l[6]+DIF1} Rainfall.Additionally, around {l[5]-1} ph scale is ideal for {fin.upper()}.'
    context = {'name':f'Suitable Crop : {fin.upper()}','d':d,'info':tstr}
    return context


def crop_disease_detetct(path):
    """
    Take the path of an image and return the disease, control, and name of the disease.

    Parameters
    ----------
        path - path of the image : str

    Example
    -------
        path = '/tmp/imgs/test.png'

    Returns
    -------
        disease_list - name and information about disease in the image : tuple
    """
    
    model = keras.models.load_model(r"static\crop_diesease_googlenet.h5")

    df = pd.read_csv(r'static\cropdis.csv')

    img = keras.utils.load_img(path,target_size=(img_height, img_width))
    img_ar = keras.utils.img_to_array(img)
    img_ar = tf.expand_dims(img_ar, 0) 

    preds = model.predict(img_ar)
    score = tf.nn.softmax(preds[0])
    lbl = np.argmax(score)

    disease_list = (df['info'][lbl],df['control'][lbl],df['name'][lbl])

    return disease_list


def days_to_months(n):
    """
    Convert days to months and days.

    Parameters
    ----------
        n - number of days : int

    Example
    -------
        n = 197

    Returns
    -------
        string - months and days
    """
    
    months = n//30
    if months == 1:
        if n%30==0:
            return f'1 month'
        return f'1 month {n%30} days'
    elif n%30 == 0:
        return f'{months} months'
    return f'{months} months {n%30} days'

def crop_yield(crop,qn):
    """
    Take the crop name and return the crop information in the form of a list.

    Parameters
    ----------
        crop - crop name : str
        qn - amount of crop in quintal : str

    Example
    -------
        crop = 'Paddy',
        qn = '9'

    Returns
    -------
        cn - list of estimated resources : list
    """

    cy = {}
    with open(r'static\CropInfo(PWGD).csv','r') as csvfile:
        csvFile = csv.reader(csvfile)
        #Skip header row
        csvFile.__next__()
        #parse CVS file into hash mapped dictionary
        for lines in csvFile:
            pr = int(lines[2])*(qn//2)
            wt1 = int(lines[3].split(' - ')[0])*(qn//2)
            wt2 = int(lines[3].split(' - ')[1])+wt1
            gp1 = int(lines[4].split('-')[0])
            gp2 = int(lines[4].split('-')[1])
            cy[lines[0]] = [f'{pr}',f'{wt1} - {wt2}',f'{days_to_months(gp1)} - {days_to_months(gp2)}']
    cn = cy[crop]
    return cn


def crop_pest_identify(path):
    """
    Given a path to an image, predict the pest and information about the pest.

    Parameters
    ----------
        path - path of the image : str

    Example
    -------
        path = '/tmp/imgs/test.png'

    Returns
    -------
        pest_list - name and information about pest in the image : tuple
    """

    model = keras.models.load_model(r"static\crop_pest_seqcnn.h5")
    pest_data = pd.read_excel(r'static\pest_info.xlsx')
    img = keras.utils.load_img(path,target_size=(img_height, img_width))
    img_ar = keras.utils.img_to_array(img)
    img_ar = tf.expand_dims(img_ar, 0) 

    preds = model.predict(img_ar)
    score = tf.nn.softmax(preds[0])
    lbl = np.argmax(score)

    pest_list = (pest_data['pest'][lbl],pest_data['info'][lbl],pest_data['control'][lbl])

    return pest_list
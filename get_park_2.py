# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 13:18:36 2021

@author: seani
"""
import googlemaps
import requests
import random
from PIL import Image


if True:
    ifile=open('index.php','w')
    for line in open('default.txt'):
        ifile.write(line)
    ifile.close()
    
    api_key = 'AIzaSyBdZXq6Tw7Pl95u7t033fzhXVlAy7aSa64'
    map_client = googlemaps.Client(api_key)
    
    #Read text file
    file=open('data.txt').read()
    file=file.split('|')
    start=file[0].strip()
    transport=['driving', 'walking', 'bicycling'][['Drive', 'Run', 'Bike'].index(file[1].strip())]
    ideal_distance=int(file[2].strip())*1000
    time=int(file[3].strip().split(' ')[0])
    dif=file[4].strip()
    #start='1999 Burdett Ave'
    #transport='walking'
    #ideal_distance=10000
    #time=20
    #dif='Easy'
    
    
    
    #find destinations
    end = []
    query = 'parks near '+start
    r = requests.get("https://maps.googleapis.com/maps/api/place/textsearch/json?" + 
                             'query=' + query + '&key=' + api_key).json()
    y = r['results']
    for i in range(len(y)):
        end.append([y[i]['formatted_address'], y[i]['name']])
    
    #choose park based on distance and mode of transportation
    end_distances = []
    for park in end:
        distance = map_client.distance_matrix(start, park[1]+' '+park[0], mode=transport)['rows'][0]['elements'][0]['distance']['value']
        end_distances.append(distance)
    differences = []
    if ideal_distance=='':
        final_park=end[end_distances.index(min(end_distances))][1]
        final_distance=min(end_distances)/1000
        park=('The nearest park is {}. Distance is {} km.'.format(final_park, final_distance))
    else:
        for i in end_distances:
            differences.append(abs(i*2-ideal_distance))
        final_park=end[differences.index(min(differences))][1]
        final_distance=end_distances[differences.index(min(differences))]*2/1000
        park=('The park that will get you closest to a {} km round trip is {}. Total distance is {} km.'.format(int(ideal_distance/1000), final_park, final_distance))
    print (park)
    
    #save data for embed link
    file2=open('embed_data.txt', 'w')
    file2.write(api_key+'\n')
    file2.write(start.replace(' ','+')+'\n')
    file2.write(final_park.replace(' ','+')+'\n')
    file2.write(transport)
    file2.close()
    
    
    
    #Producing main workout for user, create list of workouts and images
    
    #creating dictionary of lists
    core={0:['sit ups','reverse crunches','leg raises','elbow plank'],1:['bicycle crunches'],2:['flutter kicks']}
    quads={0:['lunges','high knees','lunges step-ups'],1:['side kicks'],2:['climbers','plank jump-ins']}
    glutes={0:['squats','jump knee tucks'],1:['donkey kicks','bridges','fly steps'],2:['side leg raises']}
    triceps={0:['close grip push ups','tricep dips','punches','side-to-side chops'],1:['tricep extensions'],2:['get-ups']}
    biceps={0:['doorframe rows','body rows'],1:['leg curls','chin ups'],2:['sitting pull-ups','pseudo planche']}
    back={0:['backfists','superman','alt arm/leg plank'],1:['pull-ups','star plank'],2:['alt arm/leg plank','full arch']}
    chest={0:['push-ups','chest squeezes','shoulder taps'],1:['plank rotations','shoulder press'],2:['clapping push ups']}
    workouts={0:core,1:quads,2:glutes,3:triceps,4:biceps,5:back,6:chest}
    
    #setting up time frame
    itime=time
    if time>30:
        x=time//30
        time=time-(5*x)
    sets=[]
    total=0
    while total<time:
        n=random.randint(1,4)
        if n<=time:
            total+=n
            if total>time:
                total-=n
            elif total<=time:
                sets.append(n)
                
    #using sets to create workout
    wo=[]
    for i in range(0,len(sets)):
        if dif=='Easy':
            d=0
            w=random.randint(0,6)
            wrkt_l=workouts[w][d]
            wn=random.randint(0,len(wrkt_l)-1)
            wrkt=workouts[w][d][wn]
            tup=(sets[i],wrkt)
            wo.append(tup)
        if dif=='Medium':
            d=random.randint(0,1)
            w=random.randint(0,6)
            wrkt_l=workouts[w][d]
            wn=random.randint(0,len(wrkt_l)-1)
            wrkt=workouts[w][d][wn]
            tup=(sets[i],wrkt)
            wo.append(tup)
        if dif=='Hard':
            d=random.randint(0,2)
            w=random.randint(0,6)
            wrkt_l=workouts[w][d]
            wn=random.randint(0,len(wrkt_l)-1)
            wrkt=workouts[w][d][wn]
            tup=(sets[i],wrkt)
            wo.append(tup)
        
    for i in range(0,len(wo)):
        n=i+1
        if wo[i][1]!='elbow plank' and wo[i][1]!='star plank'\
            and wo[i][1]!='alt arm/leg plank' and wo[i][1]!='full arch':
                print("{}. {}, {} sets, 10 reps".format(n,wo[i][1].title(),wo[i][0]))
        elif wo[i][1]=='elbow plank' or wo[i][1]=='star plank' or wo[i][1]=='full arch':
            print("{}. {}, {} sets, 30 sec".format(n,wo[i][1].title(),wo[i][0]))
        elif wo[i][1]=='alt arm/leg plank':
            print("{}. {}, {} sets, 15 sec each side".format(n,wo[i][1].title(),wo[i][0]))
    if itime<=30:
        print("Rest 30 seconds between each set.")
    elif itime>=30:
        print("Rest 30 seconds between each set. After every 30 minutes, rest an additional 5 minutes.")
    
    iwo=[]
    for i in range(0,len(wo)):
        iwo.append(wo[i][1])
    
    cleaned=[]
    for i in range(0,len(iwo)):
        clean=iwo[i].replace('-',' ').replace('/',' ')
        cleaned.append(clean)
    
    capped=[]
    for i in range(0,len(cleaned)):
        temp=cleaned[i].split(' ')
        if len(temp)>1:
            for n in (1,len(temp)-1):
                temp[n]=temp[n].title()
        temp=''.join(temp)
        capped.append(temp)
    
    x=len(capped)*200
    image = Image.new('RGB', (200,x))
    for i in range(0,len(capped)):
        iname=capped[i]+'.png'
        im = Image.open(iname)
        re = im.resize((200,200))
        j=i*200
        image.paste(re,(0,j))
        
    image.show()
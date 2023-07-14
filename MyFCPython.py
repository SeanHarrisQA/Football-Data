#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:32:00 2020

@author: davsu428
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def createPitchEdit(length,width, unity,linecolor): # in meters
    # Code by @JPJ_dejong

    """
    creates a plot in which the 'length' is the length of the pitch (goal to goal).
    And 'width' is the width of the pitch (sideline to sideline). 
    Fill in the unity in meters or in yards.

    """
    #Set unity
    if unity == "meters":
        # Set boundaries
        if length >= 120.5 or width >= 75.5:
            return(str("Field dimensions are too big for meters as unity, didn't you mean yards as unity?\
                       Otherwise the maximum length is 120 meters and the maximum width is 75 meters. Please try again"))
        #Run program if unity and boundaries are accepted
        else:
            #Create figure
            fig=plt.figure()
            #fig.set_size_inches(7, 5)
            ax=fig.add_subplot(1,1,1)
           
            #Pitch Outline & Centre Line
            plt.plot([0,0],[0,width], color=linecolor)
            plt.plot([0,length],[width,width], color=linecolor)
            plt.plot([length,length],[width,0], color=linecolor)
            plt.plot([length,0],[0,0], color=linecolor)
            plt.plot([(length+1.25)/2,(length+1.25)/2],[0,width], color=linecolor)
            
            #Left Penalty Area
            plt.plot([16.5 ,16.5],[(width/2 +16.5),(width/2-16.5)],color=linecolor)
            plt.plot([0,16.5],[(width/2 +16.5),(width/2 +16.5)],color=linecolor)
            plt.plot([16.5,0],[(width/2 -16.5),(width/2 -16.5)],color=linecolor)
            
            #Right Penalty Area
            plt.plot([(length-16.5),length],[(width/2 +16.5),(width/2 +16.5)],color=linecolor)
            plt.plot([(length-16.5), (length-16.5)],[(width/2 +16.5),(width/2-16.5)],color=linecolor)
            plt.plot([(length-16.5),length],[(width/2 -16.5),(width/2 -16.5)],color=linecolor)
            
            #Left 5-meters Box
            plt.plot([0,5.5],[(width/2+7.32/2+5.5),(width/2+7.32/2+5.5)],color=linecolor)
            plt.plot([5.5,5.5],[(width/2+7.32/2+5.5),(width/2-7.32/2-5.5)],color=linecolor)
            plt.plot([5.5,0.5],[(width/2-7.32/2-5.5),(width/2-7.32/2-5.5)],color=linecolor)
            
            #Right 5 -eters Box
            plt.plot([length,length-5.5],[(width/2+7.32/2+5.5),(width/2+7.32/2+5.5)],color=linecolor)
            plt.plot([length-5.5,length-5.5],[(width/2+7.32/2+5.5),width/2-7.32/2-5.5],color=linecolor)
            plt.plot([length-5.5,length],[width/2-7.32/2-5.5,width/2-7.32/2-5.5],color=linecolor)
            
            #Prepare Circles
            centreCircle = plt.Circle((length/2,width/2),9.15,color=linecolor,fill=False)
            centreSpot = plt.Circle((length/2,width/2),0.8,color=linecolor)
            leftPenSpot = plt.Circle((11,width/2),0.8,color=linecolor)
            rightPenSpot = plt.Circle((length-11,width/2),0.8,color=linecolor)
            
            #Draw Circles
            ax.add_patch(centreCircle)
            ax.add_patch(centreSpot)
            ax.add_patch(leftPenSpot)
            ax.add_patch(rightPenSpot)
            
            #Prepare Arcs
            leftArc = Arc((11,width/2),height=18.3,width=18.3,angle=0,theta1=308,theta2=52,color=linecolor)
            rightArc = Arc((length-11,width/2),height=18.3,width=18.3,angle=0,theta1=128,theta2=232,color=linecolor)
            
            #Draw Arcs
            ax.add_patch(leftArc)
            ax.add_patch(rightArc)
            #Axis titles

    #check unity again
    elif unity == "yards":
        #check boundaries again
        if length <= 95:
            return(str("Didn't you mean meters as unity?"))
        elif length >= 131 or width >= 101:
            return(str("Field dimensions are too big. Maximum length is 130, maximum width is 100"))
        #Run program if unity and boundaries are accepted
        else:
            #Create figure
            fig=plt.figure()
            #fig.set_size_inches(7, 5)
            ax=fig.add_subplot(1,1,1)
           
            #Pitch Outline & Centre Line
            plt.plot([0,0],[0,width], color=linecolor, linewidth=2.5)
            plt.plot([0,length],[width,width], color=linecolor, linewidth=2.5)
            plt.plot([length,length],[width,0], color=linecolor, linewidth=2.5)
            plt.plot([length,0],[0,0], color=linecolor, linewidth=2.5)
            plt.plot([length/2,length/2],[0,width], color=linecolor, linewidth=2.5)
            
            #Left Penalty Area
            plt.plot([18 ,18],[(width/2 +22),(width/2-22)],color=linecolor, linewidth=2.5)
            plt.plot([0,18],[(width/2 + 22),(width/2 + 22)],color=linecolor, linewidth=2.5)
            plt.plot([18,0],[(width/2 - 22),(width/2 - 22)],color=linecolor, linewidth=2.5)
            
            #Right Penalty Area
            plt.plot([(length-18),length],[(width/2 + 22),(width/2 + 22)],color=linecolor, linewidth=2.5)
            plt.plot([(length-18), (length-18)],[(width/2 +22),(width/2-22)],color=linecolor, linewidth=2.5)
            plt.plot([(length-18),length],[(width/2 -22),(width/2 -22)],color=linecolor, linewidth=2.5)
            
            #Left 6-yard Box
            plt.plot([0,6],[(width/2+7.32/2+6),(width/2+7.32/2+6)],color=linecolor, linewidth=2.5)
            plt.plot([6,6],[(width/2+7.32/2+6),(width/2-7.32/2-6)],color=linecolor, linewidth=2.5)
            plt.plot([6,0],[(width/2-7.32/2-6),(width/2-7.32/2-6)],color=linecolor, linewidth=2.5)
            
            #Right 6-yard Box
            plt.plot([length,length-6],[(width/2+7.32/2+6),(width/2+7.32/2+6)],color=linecolor, linewidth=2.5)
            plt.plot([length-6,length-6],[(width/2+7.32/2+6),width/2-7.32/2-6],color=linecolor, linewidth=2.5)
            plt.plot([length-6,length],[(width/2-7.32/2-6),width/2-7.32/2-6],color=linecolor, linewidth=2.5)
            
            #Prepare Circles; 10 yards distance. penalty on 12 yards
            centreCircle = plt.Circle(((length+1.25)/2,(width+1.25)/2),10,color=linecolor,fill=False, linewidth=2.5)
            centreSpot = plt.Circle((length/2,width/2),0.8,color=linecolor)
            leftPenSpot = plt.Circle((12,width/2),0.8,color=linecolor)
            rightPenSpot = plt.Circle((length-12,width/2),0.8,color=linecolor)
            
            #Draw Circles
            ax.add_patch(centreCircle)
            ax.add_patch(centreSpot)
            ax.add_patch(leftPenSpot)
            ax.add_patch(rightPenSpot)
            
            #Prepare Arcs
            leftArc = Arc((11,width/2),height=20,width=20,angle=0,theta1=312,theta2=48,color=linecolor, linewidth=1.5)
            rightArc = Arc((length-11,width/2),height=20,width=20,angle=0,theta1=130,theta2=230,color=linecolor, linewidth=1.5)
            
            #Draw Arcs
            ax.add_patch(leftArc)
            ax.add_patch(rightArc)
                
    #Tidy Axes
    plt.axis('off')
    
    return fig,ax

def createHalf(length, width, unity, linecolor):
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    max_x = width
    max_y = length / 2

    # Pitch outline
    plt.plot([0,max_x], [0, 0], color=linecolor)
    plt.plot([max_x, max_x], [0, max_y], color=linecolor)
    plt.plot([max_x, 0], [max_y, max_y], color=linecolor)
    plt.plot([0, 0], [max_y, 0], color=linecolor)

    # Plot penalty area
    plt.plot([18, 62],[max_y-18, max_y-18], color=linecolor)
    plt.plot([18, 18],[max_y-18, max_y], color=linecolor)
    plt.plot([62, 62],[max_y-18, max_y], color=linecolor)

    # Plot 6 yard box
    plt.plot([max_x/2-4-6, max_x/2+4+6],[max_y-6, max_y-6], color=linecolor)
    plt.plot([max_x/2-4-6, max_x/2-4-6],[max_y-6, max_y], color=linecolor)
    plt.plot([max_x/2+4+6, max_x/2+4+6],[max_y-6, max_y], color=linecolor)

    # Plot goal
    plt.plot([max_x/2-4, max_x/2+4],[max_y+2.7, max_y+2.7], color=linecolor)
    plt.plot([max_x/2-4, max_x/2-4],[max_y+2.7, max_y], color=linecolor)
    plt.plot([max_x/2+4, max_x/2+4],[max_y+2.7, max_y], color=linecolor)

    # circles
    penSpot = plt.Circle((max_x/2, max_y-12),0.8,color=linecolor)
    ax.add_patch(penSpot)
    #Prepare Arcs
    arc = Arc((max_x/2,max_y-18+6.5),height=20,width=20,angle=90,theta1=130,theta2=230,color=linecolor)
    ax.add_patch(arc)
    centreCircle = Arc((max_x/2, 0),height=20,width=20,angle=0,theta1=0,theta2=180,color=linecolor)
    ax.add_patch(centreCircle)
    centreSpot = Arc((max_x/2, 0),height=.8,width=.8,angle=0,theta1=0,theta2=180,color=linecolor, linewidth=2)
    ax.add_patch(centreSpot)
    plt.axis('off')

    return fig, ax

def create_pitch_scaleable(length, width, linecolor, scale):
    """
    creates a plot in which the 'length' is the length of the pitch (goal to goal).
    And 'width' is the width of the pitch (sideline to sideline).
    """
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    if length >= 131 or width >= 101:
        return(str("Field dimensions are too big. Maximum length is 130, maximum width is 100"))
    
    width*=scale
    length*=scale
    #Pitch Outline & Centre Line
    plt.plot([0,0],[0,width], color=linecolor)
    plt.plot([0,length],[width,width], color=linecolor)
    plt.plot([length,length],[width,0], color=linecolor)
    plt.plot([length,0],[0,0], color=linecolor)
    plt.plot([length/2,length/2],[0,width], color=linecolor)
            
    #Left Penalty Area
    plt.plot([18*scale ,18*scale],[(width/2 +22*scale),(width/2-22*scale)],color=linecolor)
    plt.plot([0,18*scale],[(width/2 +22*scale),(width/2 +22*scale)],color=linecolor)
    plt.plot([18*scale,0],[(width/2 -22*scale),(width/2 -22*scale)],color=linecolor)
            
    #Right Penalty Area
    plt.plot([(length-18*scale),length],[(width/2 +22*scale),(width/2 +22*scale)],color=linecolor)
    plt.plot([(length-18*scale), (length-18*scale)],[(width/2 + 22*scale),(width/2-22*scale)],color=linecolor)
    plt.plot([(length-18*scale),length],[(width/2 - 22*scale),(width/2 -22*scale)],color=linecolor)
            
    #Left 6-yard Box
    plt.plot([0,6*scale],[(width/2+4*scale+6*scale),(width/2+4*scale+6*scale)],color=linecolor)
    plt.plot([6*scale,6*scale],[(width/2+4*scale+6*scale),(width/2-4*scale-6*scale)],color=linecolor)
    plt.plot([6*scale,0],[(width/2-4*scale-6*scale),(width/2-4*scale-6*scale)],color=linecolor)
            
    #Right 6-yard Box
    plt.plot([length,length-6*scale],[(width/2+4*scale+6*scale),(width/2+4*scale+6*scale)],color=linecolor)
    plt.plot([length-6*scale,length-6*scale],[(width/2+4*scale+6*scale),width/2-4*scale-6*scale],color=linecolor)
    plt.plot([length-6*scale,length],[(width/2-4*scale-6*scale),width/2-4*scale-6*scale],color=linecolor)
            
    #Prepare Circles; 10 yards distance. penalty on 12 yards
    centreCircle = plt.Circle((length/2,width/2), 10*scale, fill=False, color=linecolor)
    centreSpot = plt.Circle((length/2,width/2),0.8*scale,color=linecolor)
    leftPenSpot = plt.Circle((12*scale,width/2),0.8*scale,color=linecolor)
    rightPenSpot = plt.Circle((length-12*scale,width/2),0.8*scale,color=linecolor)
            
    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)
            
    #Prepare Arcs
    leftArc = Arc((11.5*scale,width/2),height=20*scale,width=20*scale,angle=0,theta1=312,theta2=48,color=linecolor)
    rightArc = Arc((length-11.5*scale,width/2),height=20*scale,width=20*scale,angle=0,theta1=130,theta2=230,color=linecolor)
            
    #Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

    plt.axis('off')
    return fig, ax
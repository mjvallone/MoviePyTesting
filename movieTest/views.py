from moviepy.video.io.ffmpeg_tools import ffmpeg_resize
import os
import random
import numpy as np
from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips, ImageClip, AudioFileClip, clips_array
from moviepy.video.tools.segmenting import findObjects
import moviepy.audio.fx.all as afx
import moviepy.video.fx.all as vfx
from django.http import HttpResponse
from django.template.response import TemplateResponse
from scipy.ndimage import gaussian_filter


def index(request):
    response = TemplateResponse(request, 'create_videos_menu.html', {})
    return response	


def create_video(request):
    screensize = (720,460)
    txtClip = TextClip('Cool effect', color='white', font="Amiri-Bold",
                       kerning=5, fontsize=100)
    cvc = CompositeVideoClip( [txtClip.set_pos('center')],
                              size=screensize)

	# THE NEXT FOUR FUNCTIONS DEFINE FOUR WAYS OF MOVING THE LETTERS

	# helper function
    rotMatrix = lambda a: np.array( [[np.cos(a),np.sin(a)],
                                     [-np.sin(a),np.cos(a)]] )

    def vortex(screenpos,i,nletters):
		d = lambda t : 1.0/(0.3+t**8) #damping
		a = i*np.pi/ nletters # angle of the movement
		v = rotMatrix(a).dot([-1,0])
		if i%2 : v[1] = -v[1]
		return lambda t: screenpos+400*d(t)*rotMatrix(0.5*d(t)*a).dot(v)

    def cascade(screenpos,i,nletters):
		v = np.array([0,-1])
		d = lambda t : 1 if t<0 else abs(np.sinc(t)/(1+t**4))
		return lambda t: screenpos+v*400*d(t-0.15*i)

    def arrive(screenpos,i,nletters):
		v = np.array([-1,0])
		d = lambda t : max(0, 3-3*t)
		return lambda t: screenpos-400*v*d(t-0.2*i)

    def vortexout(screenpos,i,nletters):
		d = lambda t : max(0,t) #damping
		a = i*np.pi/ nletters # angle of the movement
		v = rotMatrix(a).dot([-1,0])
		if i%2 : v[1] = -v[1]
		return lambda t: screenpos+400*d(t-0.1*i)*rotMatrix(-0.2*d(t)*a).dot(v)

	# WE USE THE PLUGIN findObjects TO LOCATE AND SEPARATE EACH LETTER

    letters = findObjects(cvc) # a list of ImageClips

	# WE ANIMATE THE LETTERS

    def moveLetters(letters, funcpos):
		return [ letter.set_pos(funcpos(letter.screenpos,i,len(letters)))
				  for i,letter in enumerate(letters)]

    clips = [ CompositeVideoClip(moveLetters(letters,funcpos),
								  size = screensize).subclip(0,5)
			  for funcpos in [vortex, cascade, arrive, vortexout] ]

	# WE CONCATENATE EVERYTHING AND WRITE TO A FILE

    final_clip = concatenate_videoclips(clips)
    audio_clip = AudioFileClip("media/music.aac").subclip(0, final_clip.duration)
    final_clip = final_clip.set_audio(audio_clip).afx(afx.audio_fadeout, 1.0)

    #final_clip = vfx.resize(final_clip, (570, 570))

    final_clip.write_videofile('videos/coolTextEffects.mp4',
                               fps=23, codec='libx264',
                               audio_bitrate='1000k', bitrate='4000k')

    #final_clip.write_gif('videos/coolGif.gif', fps=23)

    html = "<html><body><div>Video successfully created<div><a href='http://localhost:8000'><button>Back</button></a></body></html>"
    return HttpResponse(html)


def create_simple_video(request):
    #load images
    image1 = ImageClip("media/real pics/1.jpeg").set_duration(2)
    image2 = ImageClip("media/real pics/2.jpeg").set_duration(2)
    image3 = ImageClip("media/real pics/3.jpeg").set_duration(2)
    image4 = ImageClip("media/real pics/4.jpeg").set_duration(2)
    image5 = ImageClip("media/real pics/5.jpeg").set_duration(2)
    image6 = ImageClip("media/real pics/6.jpeg").set_duration(2)
    image7 = ImageClip("media/real pics/7.jpeg").set_duration(2)
    image8 = ImageClip("media/real pics/8.jpeg").set_duration(2)
    image9 = ImageClip("media/real pics/9.jpeg").set_duration(2)
    image10 = ImageClip("media/real pics/10.jpeg").set_duration(2)

    #concatenate clips, play one clip after the other

    image_clips = concatenate_videoclips([image1.fadein(.5).fadeout(.5),
                                         image2.fadein(.5).fadeout(.5),
                                         image3.fadein(.5).fadeout(.5),
                                         image4.fadein(.5).fadeout(.5),
                                         image5.fadein(.5).fadeout(.5),
                                         image6.fadein(.5).fadeout(.5),
                                         image7.fadein(.5).fadeout(.5),
                                         image8.fadein(.5).fadeout(.5),
                                         image9.fadein(.5).fadeout(.5),
                                         image10.fadein(.5).fadeout(.5)])

    title_clip = (TextClip("Just Back From...", fontsize=35,
                    font="Century-Schoolbook-Roman", color="white", kerning=-2, interline=-1,
                    bg_color='#e04400', method='caption', align='center', size=(image_clips.w, image_clips.h))
                 .margin(top=5, opacity=0)
                 .set_duration(3).fadein(.5).fadeout(.5)
                 .set_position(("center", "top")))

    stats_clip = (TextClip("See Santi's recent trip of 1,836 round trip miles, with stops..", fontsize=35,
                          font="Century-Schoolbook-Roman", color="white", kerning=-2, interline=-1,
                          bg_color='#e04400', method='caption', align='center', size=(image_clips.w, image_clips.h))
                         .margin(top=5, opacity=0)
                         .set_duration(3).fadein(.5).fadeout(.5)
                         .set_position(("center", "top")))

    final_clip = concatenate_videoclips([title_clip, image_clips, stats_clip], method="compose", padding=-1)
    audio_clip = AudioFileClip("media/music.aac").subclip(0, final_clip.duration)
    final_clip = final_clip.set_audio(audio_clip).afx(afx.audio_fadeout, 1.0)

    final_clip.write_videofile('videos/myPicsVideo.mp4',
                                                 fps=23, codec='libx264',
                                                audio_bitrate='1000k', bitrate='4000k')

    html = "<html><body><div>Video successfully created<div><a href='http://localhost:8000'><button>Back</button></a></body></html>"

    return HttpResponse(html)


def create_photo_quality_video(request):
    #load images
    image1 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))
    image2 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))
    image3 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))
    image4 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))
    image5 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))
    image6 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))
    image7 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))
    image8 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))
    image9 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))
    image10 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/")))

    #concatenate clips, play one clip after the other
    image_clips = concatenate_videoclips([image3.set_duration(2.5),
                                         image4.set_duration(2.5),
                                         image5.set_duration(2.5),
                                         image6.set_duration(2.5),
                                         image7.set_duration(2.5),
                                         image8.set_duration(2.5)])

    title_image_clips = concatenate_videoclips([image1.set_duration(2.5),
                                                image2.set_duration(2.5)])

    txt_title = (TextClip("Just Back From...Santiago, Chile", fontsize=80,
                    font="Century-Schoolbook-Roman", color="white")
                 .margin(top=5, opacity=0)
                 .set_duration(5)
                 .set_position(("center", "top")))

    title_clip = (CompositeVideoClip([title_image_clips, txt_title])
             .fadein(0.5).fadeout(0.5))

    stats_image_clips = concatenate_videoclips([image9.set_duration(2.5),
                                                image10.set_duration(2.5)])

    txt_stats = (TextClip("See Santi's recent trip of 1,836 round trip miles, \n with stops..", fontsize=80,
                          font="Century-Schoolbook-Roman", color="white")
                         .margin(top=5, opacity=0)
                         .set_duration(5)
                         .set_position(("center", "top")))

    stats_clip = (CompositeVideoClip([stats_image_clips, txt_stats])
                  .fadein(.5).fadeout(.5))

    final_clip = concatenate_videoclips([title_clip, image_clips, stats_clip], method="compose")
    audio_clip = AudioFileClip("media/music.aac").subclip(0, final_clip.duration)
    final_clip = final_clip.set_audio(audio_clip).afx(afx.audio_fadeout, 1.0)

    final_clip.write_videofile('videos/randomBoastablepicsVideo.mp4',
                                     fps=23, codec='libx264',
                                    audio_bitrate='1000k', bitrate='4000k')

    html = "<html><body><div>Video successfully created<div><a href='http://localhost:8000'><button>Back</button></a></body></html>"

    return HttpResponse(html)


def blur(image):
    """ Returns a blurred (radius=2 pixels) version of the image """
    return gaussian_filter(image.astype(float), sigma=2)


def create_overall_quality_video(request):
    #load images
    image1 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')
    image2 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')
    image3 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')
    image4 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')
    image5 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')
    image6 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')
    image7 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')
    image8 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')
    image9 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')
    image10 = ImageClip("media/real pics/"+random.choice(os.listdir("media/real pics/"))).set_pos('center')

    #calculate max width and height
    images = []
    images.extend([image1, image2, image3, image4, image5, image6, image7, image8, image9, image10])
    max_width = 0
    max_height = 0
    for img in images:
        if img.size[0] > max_width:
            max_width = img.size[0]
        if img.size[1] > max_height:
            max_height = img.size[1]

    #create blurred images
    image1 = CompositeVideoClip([image1.resize((max_width, max_height)).fl_image(blur), image1.resize(.9)])
    image2 = CompositeVideoClip([image2.resize((max_width, max_height)).fl_image(blur), image2.resize(.9)])
    image3 = CompositeVideoClip([image3.resize((max_width, max_height)).fl_image(blur), image3.resize(.9)])
    image4 = CompositeVideoClip([image4.resize((max_width, max_height)).fl_image(blur), image4.resize(.9)])
    image5 = CompositeVideoClip([image5.resize((max_width, max_height)).fl_image(blur), image5.resize(.9)])
    image6 = CompositeVideoClip([image6.resize((max_width, max_height)).fl_image(blur), image6.resize(.9)])
    image7 = CompositeVideoClip([image7.resize((max_width, max_height)).fl_image(blur), image7.resize(.9)])
    image8 = CompositeVideoClip([image8.resize((max_width, max_height)).fl_image(blur), image8.resize(.9)])
    image9 = CompositeVideoClip([image9.resize((max_width, max_height)).fl_image(blur), image9.resize(.9)])
    image10 = CompositeVideoClip([image10.resize((max_width, max_height)).fl_image(blur), image10.resize(.9)])

    #concatenate clips, play one clip after the other
    image_clips = concatenate_videoclips([image1.set_duration(2).fadein(.5).fadeout(.5),
                                         image2.set_duration(2).fadein(.5).fadeout(.5),
                                         image3.set_duration(2).fadein(.5).fadeout(.5),
                                         image4.set_duration(2).fadein(.5).fadeout(.5),
                                         image5.set_duration(2).fadein(.5).fadeout(.5),
                                         image6.set_duration(2).fadein(.5).fadeout(.5),
                                         image7.set_duration(2).fadein(.5).fadeout(.5),
                                         image8.set_duration(2).fadein(.5).fadeout(.5),
                                         image9.set_duration(2).fadein(.5).fadeout(.5),
                                         image10.set_duration(2).fadein(.5).fadeout(.5)])

    title_clip = (TextClip("Just Back From...", fontsize=35,
                    font="Century-Schoolbook-Roman", color="white", kerning=-2, interline=-1,
                    bg_color='#e04400', method='caption', align='center', size=(image_clips.w, image_clips.h))
                 .margin(top=5, opacity=0)
                 .set_duration(3).fadein(.5).fadeout(.5)
                 .set_position(("center", "top")))

    stats_clip = (TextClip("See Santi's recent trip of 1,836 round trip miles, with stops..", fontsize=35,
                          font="Century-Schoolbook-Roman", color="white", kerning=-2, interline=-1,
                          bg_color='#e04400', method='caption', align='center', size=(image_clips.w, image_clips.h))
                         .margin(top=5, opacity=0)
                         .set_duration(3).fadein(.5).fadeout(.5)
                         .set_position(("center", "top")))

    final_clip = concatenate_videoclips([title_clip, image_clips, stats_clip],
                                        method="compose", padding=-1)

    audio_clip = AudioFileClip("media/music.aac").subclip(0, final_clip.duration)
    final_clip = final_clip.set_audio(audio_clip).afx(afx.audio_fadeout, 1.5)


#write_videofile -> preset :
#Sets the time that FFMPEG will spend optimizing the compression.
# Choices are: ultrafast, superfast, fast, medium, slow, superslow.
# Note that this does not impact the quality of the video, only the size of the video file.
# So choose ultrafast when you are in a hurry and file size does not matter.

    final_clip.write_videofile('videos/overallQualityVideo.mp4',
                                     fps=23, codec='libx264',
                                    audio_bitrate='1000k', bitrate='4000k')

    html = "<html><body><div>Video successfully created<div><a href='http://localhost:8000'><button>Back</button></a></body></html>"

    return HttpResponse(html)

def create_presentation_video(request):
    #screensize = (720, 460)
    screensize = (1024, 780)
    txt_clip1 = TextClip('Just Back From...',
                        color='white', font="Amiri-Bold",
                       kerning=2, fontsize=50).set_position((10, 80))
    txt_clip2 = TextClip('Seville, Spain',
                        color='white', font="Amiri-Bold",
                       kerning=2, fontsize=50).set_position((10, 120))
    txt_clip3 = TextClip('Costa Brava, Spain',
                        color='white', font="Amiri-Bold",
                       kerning=2, fontsize=50).set_position((10, 160))
    txt_clip4 = TextClip('Arles, France',
                        color='white', font="Amiri-Bold",
                       kerning=2, fontsize=50).set_position((10, 200))
    txt_clip5 = TextClip('Eze, France',
                        color='white', font="Amiri-Bold",
                       kerning=2, fontsize=50).set_position((10, 240))

    #title_clip = (TextClip("Just Back From...", fontsize=35,
    #                font="Century-Schoolbook-Roman", color="white", kerning=-2, interline=-1,
    #                bg_color='#e04400', method='caption', align='center', size=(image_clips.w, image_clips.h))
    #             .margin(top=5, opacity=0)
    #             .set_duration(3).fadein(.5).fadeout(.5)
    #             .set_position(("center", "top")))

    #txt = "\n".join([
    #"Just Back From...",
    #"Seville, Spain",
    #"Costa Brava, Spain",
    #"Arles, France",
    #"Eze, France"
    #])
    #txt_clip1 = TextClip(txt, color='white', font="Amiri-Bold",
    #                   kerning=2, fontsize=50).set_position((10, 80))

    #clip_txt = TextClip(txt,color='white', align='West',fontsize=25,
    #                font='Xolonium-Bold', method='label')

    #txt_clips = clips_array([[txt_clip1, txt_clip2]])
    #cvc = CompositeVideoClip([txt_clip1, txt_clip2, txt_clip3, txt_clip4, txt_clip5],
    cvc = CompositeVideoClip([txt_clip1],
                              size=screensize)

    # helper function
    rot_matrix = lambda a: np.array([[np.cos(a), np.sin(a)],
                                     [-np.sin(a), np.cos(a)]])

    def cascade(screenpos,i,nletters):
        v = np.array([0,-1])
        d = lambda t : 1 if t<0 else abs(np.sinc(t)/(1+t**4))
        return lambda t: screenpos+v*400*d(t-0.15*i)

    def vortexout(screenpos,i,nletters):
        d = lambda t : max(0,t) #damping
        a = i*np.pi/ nletters # angle of the movement
        v = rot_matrix(a).dot([-1,0])
        if i%2 : v[1] = -v[1]
        return lambda t: screenpos+400*d(t-0.1*i)*rot_matrix(-0.2*d(t)*a).dot(v)

    letters = findObjects(cvc) # a list of ImageClips

    def moveLetters(letters, funcpos):
        return [ letter.set_pos(funcpos(letter.screenpos,i,len(letters)))
                  for i,letter in enumerate(letters)]

    clips = [CompositeVideoClip(moveLetters(letters, funcpos),
                                  size=screensize).subclip(0, 3)
              for funcpos in [cascade, vortexout]]

    final_clip = concatenate_videoclips(clips)
    #final_clip = vfx.resize(final_clip, (570, 570))

    final_clip.write_videofile('videos/presentationVideo.mp4',
                               fps=23, codec='libx264',
                               audio_bitrate='1000k', bitrate='4000k')

    html = "<html><body><div>Video successfully created<div><a href='http://localhost:8000'><button>Back</button></a></body></html>"
    return HttpResponse(html)

from moviepy.video.io.ffmpeg_tools import ffmpeg_resize
import os
import random
import numpy as np
from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips, ImageClip, AudioFileClip
from moviepy.video.tools.segmenting import findObjects
import moviepy.audio.fx.all as afx
from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request):
    response = TemplateResponse(request, 'create_videos_menu.html', {})
    return response	


def create_video(request):
    screensize = (720,460)
    txtClip = TextClip('Cool effect',color='white', font="Amiri-Bold",
                       kerning = 5, fontsize=100)
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

    #ffmpeg_resize(final_clip, final_clip, '570')

    final_clip.write_videofile('videos/coolTextEffects.mp4',
                               fps=23, codec='libx264',
                               audio_bitrate='1000k', bitrate='4000k')

    html = "<html><body><div>Video successfully created<div><a href='http://localhost:8000'><button>Back</button></a></body></html>"
    return HttpResponse(html)


def create_simple_video(request):
    #load images
    image1 = ImageClip("media/img1_lq.jpg")
    image2 = ImageClip("media/img2_lq.jpg")
    image3 = ImageClip("media/img3_lq.jpg")
    image4 = ImageClip("media/img4_lq.jpg")
    image5 = ImageClip("media/img5_lq.jpg")
    image6 = ImageClip("media/img6_lq.jpg")
    image7 = ImageClip("media/img7_lq.jpg")
    image8 = ImageClip("media/img8_lq.jpg")
    image9 = ImageClip("media/img9_lq.jpg")
    image10 = ImageClip("media/img10_lq.jpg")

    #concatenate clips, play one clip after the other

    image_clips = concatenate_videoclips([image3.set_duration(2.5),
                                         image4.set_duration(2.5),
                                         image5.set_duration(2.5),
                                         image6.set_duration(2.5),
                                         image7.set_duration(2.5),
                                         image8.set_duration(2.5)])

    # plays clip1, clip2 on top of clip1, and so on
    #imageClips = CompositeVideoClip([image1.set_pos("center"), #starts at t=0
    #    image2.set_start(5).crossfadein(1).set_pos("center"),
    #    image3.set_start(10).crossfadein(1.5).set_pos("center")],
    #    size=(720, 460))

    title_image_clips = concatenate_videoclips([image1.set_duration(2.5),
                                                image2.set_duration(2.5)])

    txt_title = (TextClip("Just Back From...Santiago, Chile", fontsize=100,
                    font="Century-Schoolbook-Roman", color="white")
                 .margin(top=5, opacity=90)
                 .set_duration(5)
                 .set_position(("center", "top")))

    title_clip = (CompositeVideoClip([title_image_clips, txt_title])
             .fadein(0.5).fadeout(0.5))

    stats_image_clips = concatenate_videoclips([image9.set_duration(2.5),
                                                image10.set_duration(2.5)])

    txt_stats = (TextClip("See Santi's recent trip of 1,836 round trip miles, \n with stops..", fontsize=80,
                          font="Century-Schoolbook-Roman", color="white")
                         .margin(top=5, opacity=90)
                         .set_duration(5)
                         .set_position(("center", "top")))

    stats_clip = (CompositeVideoClip([stats_image_clips, txt_stats])
                  .fadein(.5).fadeout(.5))

    final_clip = concatenate_videoclips([title_clip, image_clips, stats_clip], method="compose")
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


def create_overall_quality_video(request):
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
    image_clips = concatenate_videoclips([image1.set_duration(2),
                                         image2.set_duration(2),
                                         image3.set_duration(2),
                                         image4.set_duration(2),
                                         image5.set_duration(2),
                                         image6.set_duration(2),
                                         image7.set_duration(2),
                                         image8.set_duration(2),
                                         image9.set_duration(2),
                                         image10.set_duration(2)])

    title_clip = (TextClip("Just Back From...Santiago, Chile", fontsize=35,
                    font="Century-Schoolbook-Roman", color="white", kerning=-2, interline=-1,
                    bg_color='#e04400', method='caption', align='center', size=(image_clips.w, image_clips.h))
                 .margin(top=5, opacity=0)
                 .set_duration(3)
                 .fadein(.5)
                 .fadeout(.5)
                 .set_position(("center", "top")))

    stats_clip = (TextClip("See Santi's recent trip of 1,836 round trip miles, with stops..", fontsize=35,
                          font="Century-Schoolbook-Roman", color="white", kerning=-2, interline=-1,
                          bg_color='#e04400', method='caption', align='center', size=(image_clips.w, image_clips.h))
                         .margin(top=5, opacity=0)
                         .set_duration(3)
                         .fadein(.5)
                         .fadeout(.5)
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
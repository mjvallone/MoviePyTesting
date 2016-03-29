import numpy as np
#from moviepy.editor import *
from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips, ImageClip
from moviepy.video.tools.segmenting import findObjects
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

    clips = [ CompositeVideoClip( moveLetters(letters,funcpos),
								  size = screensize).subclip(0,5)
			  for funcpos in [vortex, cascade, arrive, vortexout] ]

	# WE CONCATENATE EVERYTHING AND WRITE TO A FILE

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile('videos/coolTextEffects.mp4',fps=23, codec='libx264', bitrate='4000k')

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
    image_clips = concatenate_videoclips([#image1.set_duration(2.5),
                                         #image2.set_duration(2.5),
                                         image3.set_duration(2.5),
                                         image4.set_duration(2.5),
                                         image5.set_duration(2.5),
                                         image6.set_duration(2.5),
                                         image7.set_duration(2.5),
                                         image8.set_duration(2.5),
                                         image9.set_duration(2.5),
                                         image10.set_duration(2.5)])

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
             .set_duration(5).fadein(0.5).fadeout(0.5))

    #final_clip = ImageClip("media/black.png")
    #stats_image_clips = concatenate_videoclips([final_clip.set_duration(3)])
    #txt_stats = (TextClip("See Santi's recent trip of 1,836 round trip miles, with stops..", fontsize=100,font="Century-Schoolbook-Roman", color="white")
    #             .margin(top=20, opacity=90).set_position("center"))

    #stats_clip = (CompositeVideoClip([stats_image_clips, txt_stats]).set_duration(3).fadein(0.5).fadeout(0.5))

    final_clip = concatenate_videoclips([title_clip, image_clips])
    final_clip.set_duration(30).write_videofile('videos/simpleTextAndImagesVideo.mp4',
                                               fps=30, codec='libx264') #, bitrate='4000k'

    html = "<html><body><div>Video successfully created<div><a href='http://localhost:8000'><button>Back</button></a></body></html>"

    return HttpResponse(html)


def create_photo_quality_video(request):
    #load images
    trip_presentation = ImageClip("media/trip_presentation.png")
    image1 = ImageClip("media/img1_hq.jpg")
    image2 = ImageClip("media/img2_hq.jpg")
    image3 = ImageClip("media/img3_hq.jpg")
    image4 = ImageClip("media/img4_hq.jpg")
    image5 = ImageClip("media/img5_hq.jpg")
    image6 = ImageClip("media/img6_hq.jpg")
    image7 = ImageClip("media/img7_hq.jpg")
    image8 = ImageClip("media/img8_hq.jpg")
    image9 = ImageClip("media/img9_hq.jpg")
    image10 = ImageClip("media/img10_hq.jpg")
    trip_stats = ImageClip("media/trip_stats.png")

    #concatenate clips, play one clip after the other
    image_clips = concatenate_videoclips([#trip_presentation.set_duration(2.5),
                                         #image1.set_duration(2.5),
                                         #image2.set_duration(2.5),
                                         image3.set_duration(2.5),
                                         image4.set_duration(2.5),
                                         image5.set_duration(2.5),
                                         image6.set_duration(2.5),
                                         image7.set_duration(2.5),
                                         image8.set_duration(2.5),
                                         image9.set_duration(2.5),
                                         image10.set_duration(2.5)])
                                         #trip_stats.set_duration(2.5)])

    # plays clip1, clip2 on top of clip1, and so on
    #imageClips = CompositeVideoClip([image1.set_pos("center"), #starts at t=0
    #    image2.set_start(5).crossfadein(1).set_pos("center"),
    #    image3.set_start(10).crossfadein(1.5).set_pos("center")],
    #    size=(720, 460))

    title_image_clips = concatenate_videoclips([image1.set_duration(2.5),
                                                image2.set_duration(2.5)])

    txt_title = (TextClip("Just Back From...Santiago, Chile", fontsize=100,
                    font="Century-Schoolbook-Roman", color="white")
                 .margin(top=30, opacity=100)
                 .set_duration(5)
                 .set_position(("center", "top")))

    title_clip = (CompositeVideoClip([title_image_clips, txt_title])
                  .set_duration(5).fadein(0.5).fadeout(.5))

    #stats_image_clips = concatenate_videoclips([image9.set_duration(2.5), image10.set_duration(2.5)])

    #txt_stats = (TextClip("See Santi's recent trip of 1,836 round trip miles, with stops..", fontsize=100,font="Century-Schoolbook-Roman", color="white")
    #             .margin(top=30, opacity=100).set_position(("center", "top")))

    #stats_clip = (CompositeVideoClip([stats_image_clips, txt_stats]).set_duration(5).fadein(.5).fadeout(.5))

    image_clips = concatenate_videoclips([title_clip, image_clips])
    image_clips.set_duration(25).write_videofile('videos/photoQualityVideo.mp4',
                                               fps=30, codec='libx264') #, bitrate='4000k'

    html = "<html><body><div>Video successfully created<div><a href='http://localhost:8000'><button>Back</button></a></body></html>"

    return HttpResponse(html)


def create_overall_quality_video(request):
    #load images
    trip_presentation = ImageClip("media/trip_presentation.png")
    image1 = ImageClip("media/img1_hq.jpg")
    image2 = ImageClip("media/img2_hq.jpg")
    image3 = ImageClip("media/img3_hq.jpg")
    image4 = ImageClip("media/img4_hq.jpg")
    image5 = ImageClip("media/img5_hq.jpg")
    image6 = ImageClip("media/img6_hq.jpg")
    image7 = ImageClip("media/img7_hq.jpg")
    image8 = ImageClip("media/img8_hq.jpg")
    image9 = ImageClip("media/img9_hq.jpg")
    image10 = ImageClip("media/img10_hq.jpg")
    trip_stats = ImageClip("media/trip_stats.png")

    #concatenate clips, play one clip after the other
    image_clips = concatenate_videoclips([#trip_presentation.set_duration(2.5),
                                         #image1.set_duration(2.5),
                                         #image2.set_duration(2.5),
                                         image3.set_duration(2.5),
                                         image4.set_duration(2.5),
                                         image5.set_duration(2.5),
                                         image6.set_duration(2.5),
                                         image7.set_duration(2.5),
                                         image8.set_duration(2.5),
                                         image9.set_duration(2.5),
                                         image10.set_duration(2.5)])
                                         #trip_stats.set_duration(2.5)])

    # plays clip1, clip2 on top of clip1, and so on
    #imageClips = CompositeVideoClip([image1.set_pos("center"), #starts at t=0
    #    image2.set_start(5).crossfadein(1).set_pos("center"),
    #    image3.set_start(10).crossfadein(1.5).set_pos("center")],
    #    size=(720, 460))

    title_image_clips = concatenate_videoclips([image1.set_duration(2.5),
                                                image2.set_duration(2.5)])

    txt_title = (TextClip("Just Back From...Santiago, Chile", fontsize=100,
                    font="Century-Schoolbook-Roman", color="white")
                 .margin(top=30, opacity=100)
                 .set_position(("center", "top")))

    title_clip = (CompositeVideoClip([title_image_clips, txt_title])
             .set_duration(5)
             .fadein(0.5)
             .fadeout(.5))

    stats_image_clips = concatenate_videoclips([image9.set_duration(2.5),
                                                image10.set_duration(2.5)])

    txt_stats = (TextClip("See Santi's recent trip of 1,836 round trip miles, with stops..", fontsize=100,
                    font="Century-Schoolbook-Roman", color="white")
                 .margin(top=30, opacity=100)
                 .set_position(("center", "top")))

    stats_clip = (CompositeVideoClip([stats_image_clips, txt_stats])
             .set_duration(5)
             .fadein(.5)
             .fadeout(.5))

    image_clips = concatenate_videoclips([title_clip, image_clips])
    image_clips.set_duration(25).write_videofile('videos/photoQualityVideo.mp4',
                                               fps=30,
                                               codec='mpeg4')

    html = "<html><body><div>Video successfully created<div><a href='http://localhost:8000'><button>Back</button></a></body></html>"

    return HttpResponse(html)
#from __future__ import print_function
import sys, fsdk, math, ctypes, time
from fsdk import FSDK
import mysql.connector
import datetime
import time



#from __future__ import print_function
import sys, fsdk, math, ctypes, time
from fsdk import FSDK
import mysql.connector
import datetime
import time
from PIL import Image
import PIL




license_key = "fVrFCzYC5wOtEVspKM/zfLWVcSIZA4RNqx74s+QngdvRiCC7z7MHlSf2w3+OUyAZkTFeD4kSpfVPcRVIqAKWUZzJG975b/P4HNNzpl11edXGIyGrTO/DImoZksDSRs6wktvgr8lnNCB5IukIPV5j/jBKlgL5aqiwSfyCR8UdC9s="

if not fsdk.windows:
	print('The program is for Microsoft Windows.'); exit(1)
import win

trackerMemoryFile = "tracker70.dat"

FONT_SIZE = 30

print("Initializing FSDK... ", end='')
FSDK.ActivateLibrary(license_key);
FSDK.Initialize()
print("OK\nLicense info:", FSDK.GetLicenseInfo())

FSDK.InitializeCapturing()
print('Looking for video cameras... ', end = '')
camList = FSDK.ListCameraNames()

if not camList: print("Please attach a camera.");
print(camList[0]) # camList[0].devicePath

camera = camList[0] # choose the first camera (0)
print("using '%s'" % camera)
formatList = FSDK.ListVideoFormats(camera)
#print(*zip(range(len(formatList)), formatList), sep='\n')
print(*formatList[0:5], sep='\n')
if len(formatList)>5: print('...', len(formatList)-5, 'more formats (skipped)...')

vfmt = formatList[0] # choose the first format: vfmt.Width, vfmt.Height, vfmt.BPP
print('Selected camera format:', vfmt)
FSDK.SetVideoFormat(camera, vfmt)

print("Trying to open '%s'... " % camera, end = '')
camera = FSDK.OpenVideoCamera(camera)
print("OK", camera.handle)

try:
	fsdkTracker = FSDK.Tracker.FromFile(trackerMemoryFile)
except:
	fsdkTracker = FSDK.Tracker()  # creating a FSDK Tracker

fsdkTracker.SetParameters( # set realtime face detection parameters
	RecognizeFaces=True, DetectFacialFeatures=True,
	HandleArbitraryRotations=True, DetermineFaceRotationAngle=False,
	InternalResizeWidth=256, FaceDetectionThreshold=5
)

need_to_exit = False


def WndProc(hWnd, message, wParam, lParam):
	global capturedFace
	if message == win.WM_CTLCOLOREDIT:
		fsdkTracker.SetName(capturedFace, win.GetWindowText(inpBox))
	if message == win.WM_DESTROY:
		global need_to_exit
		need_to_exit = True
	else:
		if message == win.WM_MOUSEMOVE:
			updateActiveFace()
			return 1
		if message == win.WM_LBUTTONDOWN:
			if activeFace and capturedFace != activeFace:
				capturedFace = activeFace
				win.SetWindowText(inpBox, fsdkTracker.GetName(capturedFace))
				win.ShowWindow(inpBox, win.SW_SHOW)
				win.SetFocus(inpBox)
			else:
				capturedFace = None
				win.ShowWindow(inpBox, win.SW_HIDE)
			return 1
	return win.DefWindowProc(hWnd, message, win.WPARAM(wParam), win.LPARAM(lParam))

wcex = win.WNDCLASSEX(cbSize = ctypes.sizeof(win.WNDCLASSEX), style = 0, lpfnWndProc = win.WNDPROC(WndProc),
	cbClsExtra = 0, cbWndExtra = 0,	hInstance = 0, hIcon = 0, hCursor = win.LoadCursor(0, win.IDC_ARROW), hbrBackground = 0,
	lpszMenuName = 0, lpszClassName = win.L("My Window Class"), hIconSm = 0)
win.RegisterClassEx(wcex)

hwnd = win.CreateWindowEx(win.WS_EX_CLIENTEDGE, win.L("My Window Class"), win.L("Live Recognition"), win.WS_SYSMENU | win.WS_CAPTION | win.WS_CLIPCHILDREN,
	50, 50, vfmt.Width, vfmt.Height, *[0]*4)
win.ShowWindow(hwnd, win.SW_SHOW)

# textBox = win.CreateWindow(win.L("STATIC"), win.L("Click face to name it"), win.SS_CENTER | win.WS_CHILD, 0, 0, 0, 0, hwnd, 0, 0, 0)
# myFont = win.CreateFont(30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, win.L("Microsoft Sans Serif"))
# win.SendMessage(textBox, win.WM_SETFONT, myFont, True);
# win.SetWindowPos(textBox, 0, 0, vfmt.Height, vfmt.Width, 80, win.SWP_NOZORDER)
# win.ShowWindow(textBox, win.SW_SHOW)

inpBox = win.CreateWindow(win.L("EDIT"), win.L(""), win.SS_CENTER | win.WS_CHILD, 0, 0, 0, 0, hwnd, 0, 0, 0)
myFont = win.CreateFont(30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, win.L("Microsoft Sans Serif"))
win.SendMessage(inpBox, win.WM_SETFONT, myFont, True);
win.SetWindowPos(inpBox, 0, 0, vfmt.Height-80, vfmt.Width, 80, win.SWP_NOZORDER)
win.UpdateWindow(hwnd)

def dot_center(dots): # calc geometric center of dots
	return sum(p.x for p in dots)/len(dots), sum(p.y for p in dots)/len(dots)



class LowPassFilter: # low pass filter to stabilize frame size
	def __init__(self, a = 0.35): self.a, self.y = a, None
	def __call__(self, x): self.y = self.a * x + (1-self.a)*(self.y or x); return self.y

class FaceLocator:
	def __init__(self, fid):
		self.lpf = None
		self.center = self.angle = self.frame = None
		self.fid = fid
	def isIntersect(self, state):
		(x1,y1,x2,y2), (xx1,yy1,xx2,yy2) = self.frame, state.frame
		return not(x1 >= xx2 or x2 < xx1 or y1 >= yy2 or y2 < yy1)
	def isActive(self): return self.lpf is not None
	def is_inside(self, x, y):
		x -= self.center[0]; y -= self.center[1]
		a = self.angle * math.pi / 180
		x, y = x*math.cos(a) + y*math.sin(a), x*math.sin(a) - y*math.cos(a)
		return (x/self.frame[0])**2 + (y/self.frame[1])**2 <= 1
	def draw_shape(self, surf):
		container = surf.beginContainer()
		surf.translateTransform(*self.center).rotateTransform(self.angle).ellipse(facePen, *self.frame) # draw frame
		if activeFace == self.fid:
			surf.ellipse(faceActivePen, *self.frame) # draw active frame
		if capturedFace == self.fid:
			surf.ellipse(faceCapturedPen, *self.frame) # draw captured frame
		surf.endContainer(container)

	def draw(self, surf, path, face_id=None):
		if face_id is not None:
			ff = fsdkTracker.GetFacialFeatures(0, face_id)
			if self.lpf is None: self.lpf = LowPassFilter()
			xl, yl = dot_center([ff[k] for k in FSDK.FSDKP_LEFT_EYE_SET])
			xr, yr = dot_center([ff[k] for k in FSDK.FSDKP_RIGHT_EYE_SET])
			w = self.lpf((xr - xl)*2.8)
			h = w*1.4
			self.center = (xr + xl)/2, (yr + yl)/2 + w*0.05
			self.angle = math.atan2(yr-yl, xr-xl)*180/math.pi
			self.frame = -w/2, -h/2, w/2, h/2

			self.draw_shape(surf)

			name = fsdkTracker.GetName(self.fid)
			#print(name)
			surf.drawString(name, font, self.center[0]-w/2+2, self.center[1]-h/2+2, text_shadow)
			surf.drawString(name, font, self.center[0]-w/2, self.center[1]-h/2, text_color)
		else:
			if self.lpf is not None: self.lpf, self.countdown = None, 35
			self.countdown -= 1
			if self.countdown <= 8:
				self.frame = [v * 0.95 for v in self.frame]
			else:
				self.draw_shape(surf)
			name='Unkown User!';
			#print(name)

		path.ellipse(*self.frame) # frame background
		return self.lpf or self.countdown > 0

activeFace = capturedFace = None
def updateActiveFace():
	global activeFace
	p = win.ScreenToClient(hwnd, win.GetCursorPos() )
	for fid, tr in trackers.items():
		if tr.is_inside(p.x, p.y):
			activeFace = fid
			break
	else: activeFace = None

gdiplus = win.GDIPlus() # initialize GDI+
graphics = win.Graphics(hwnd=hwnd)
backsurf = win.Bitmap.FromGraphics(vfmt.Width, vfmt.Height, graphics)
surfGr = win.Graphics(bmp=backsurf).setSmoothing(True) # graphics object for back surface with antialiasing
facePen, featurePen, brush = win.Pen(0x60ffffff, 5), win.Pen(0xa060ff60, 1.8), win.Brush(0x28ffffff)
faceActivePen, faceCapturedPen = win.Pen(0xFF00ff00, 2), win.Pen(0xFFff0000, 3)
font = win.Font(win.FontFamily("Tahoma"), FONT_SIZE)
text_color, text_shadow = win.Brush(0xffffffff), win.Brush(0xff808080)

trackers = {}
def att():
    pass
def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")




sampleNum = 0
while 1:
	sampleNum = sampleNum + 1
	img = camera.GrabFrame()
	surfGr.resetClip().drawImage(win.Bitmap.FromHBITMAP(img.GetHBitmap())) # fill backsurface with image

	faces = frozenset(fsdkTracker.FeedFrame(0, img)) # recognize all faces in the image
	for face_id in faces.difference(trackers): trackers[face_id] = FaceLocator(face_id) # create new trackers

	missed, gpath = [], win.GraphicsPath()
	for face_id, tracker in trackers.items(): # iterate over current trackers
		ss = fsdkTracker.GetName(face_id)
		if sampleNum > 50:
			ts = time.time()
			date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
			timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
			conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceiotdb')
			cursor = conn.cursor()
			cursor.execute("select * from regtb where UserName='" + str(ss) + "' ")
			data = cursor.fetchone()
			if data is None:
				print("No Face Info Found")

				# from playsound import playsound

				sendmsg("9655034039","Face Decect!")

				import winsound

				filename = 'alert.wav'
				winsound.PlaySound(filename, winsound.SND_FILENAME)

				outFileName = 'static/out.jpg'

				bmp = win.Bitmap.FromHBITMAP(img.GetHBitmap())

				saimg = FSDK.Image(bmp.GetHBITMAP())
				saimg.SaveToFile(outFileName, quality=85)

				import smtplib
				from email.mime.multipart import MIMEMultipart
				from email.mime.text import MIMEText
				from email.mime.base import MIMEBase
				from email import encoders

				fromaddr = "projectmailm@gmail.com"
				toaddr = "devadharshiniakshaya@gmail.com"

				# instance of MIMEMultipart
				msg = MIMEMultipart()

				# storing the senders email address
				msg['From'] = fromaddr

				# storing the receivers email address
				msg['To'] = toaddr

				# storing the subject
				msg['Subject'] = "Face Detection"

				# string to store the body of the mail
				body = "Hai"

				# attach the body with the msg instance
				msg.attach(MIMEText(body, 'plain'))

				# open the file to be sent
				filename = "out.png"
				attachment = open("static/out.jpg", "rb")

				# instance of MIMEBase and named as p
				p = MIMEBase('application', 'octet-stream')

				# To change the payload into encoded form
				p.set_payload((attachment).read())

				# encode into base64
				encoders.encode_base64(p)

				p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

				# attach the instance 'p' to instance 'msg'
				msg.attach(p)

				# creates SMTP session
				s = smtplib.SMTP('smtp.gmail.com', 587)

				# start TLS for security
				s.starttls()

				# Authentication
				s.login(fromaddr, "qmgn xecl bkqv musr")

				# Converts the Multipart msg into a string
				text = msg.as_string()

				# sending the mail
				s.sendmail(fromaddr, toaddr, text)

				# terminating the session
				s.quit()
			else:
				conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceiotdb')
				cursor = conn.cursor()
				cursor.execute("select * from entrytb where Date='" + str(date) + "' and UserName='" + str(ss) + "'")
				data = cursor.fetchone()
				if data is None:
					conn = mysql.connector.connect(user='root', password='', host='localhost',
												   database='1faceiotdb')
					cursor = conn.cursor()
					cursor.execute(
						"insert into entrytb values('','" + ss + "','" + str(date) + "','" + str(
							timeStamp) + "','1')")
					conn.commit()
					conn.close()
					#print("Face Attendance Info Saved")
				else:
					print("Already Face Attendance Info Saved")

				sendmsg("9655034039","Criminal Face Name" + ss)

				import winsound

				filename = 'alert.wav'
				winsound.PlaySound(filename, winsound.SND_FILENAME)

				outFileName = 'static/out.jpg'

				bmp = win.Bitmap.FromHBITMAP(img.GetHBitmap())

				saimg = FSDK.Image(bmp.GetHBITMAP())
				saimg.SaveToFile(outFileName, quality=85)

				import smtplib
				from email.mime.multipart import MIMEMultipart
				from email.mime.text import MIMEText
				from email.mime.base import MIMEBase
				from email import encoders

				fromaddr = "projectmailm@gmail.com"
				toaddr = "devadharshiniakshaya@gmail.com"

				# instance of MIMEMultipart
				msg = MIMEMultipart()

				# storing the senders email address
				msg['From'] = fromaddr

				# storing the receivers email address
				msg['To'] = toaddr

				# storing the subject
				msg['Subject'] = "Face Detection"

				# string to store the body of the mail
				body = "Criminal Face Name" + ss

				# attach the body with the msg instance
				msg.attach(MIMEText(body, 'plain'))

				# open the file to be sent
				filename = "out.png"
				attachment = open("static/out.jpg", "rb")

				# instance of MIMEBase and named as p
				p = MIMEBase('application', 'octet-stream')

				# To change the payload into encoded form
				p.set_payload((attachment).read())

				# encode into base64
				encoders.encode_base64(p)

				p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

				# attach the instance 'p' to instance 'msg'
				msg.attach(p)

				# creates SMTP session
				s = smtplib.SMTP('smtp.gmail.com', 587)

				# start TLS for security
				s.starttls()

				# Authentication
				s.login(fromaddr, "qmgn xecl bkqv musr")

				# Converts the Multipart msg into a string
				text = msg.as_string()

				# sending the mail
				s.sendmail(fromaddr, toaddr, text)

				# terminating the session
				s.quit()






		if face_id in faces: tracker.draw(surfGr, gpath, face_id) #fsdkTracker.GetFacialFeatures(face_id)) # draw existing tracker
		else: missed.append(face_id)
	for mt in missed: # find and remove trackers that are not active anymore
		st = trackers[mt]
		if any(st.isIntersect(trackers[tr]) for tr in faces) or not st.draw(surfGr, gpath): del trackers[mt]

	if capturedFace not in trackers:
		capturedFace = None
		win.ShowWindow(inpBox, win.SW_HIDE)
	updateActiveFace()

	# surfGr.clipPath(gpath, win.CombineModeExclude).fillRect(brush, 0, 0, vfmt.Width, vfmt.Height) # clip frames
	graphics.drawImage(backsurf, 0, 0) # show backsurface

	#Close
	if sampleNum > 50:
		sampleNum=0
		break



	msg = win.MSG()
	if win.PeekMessage(win.byref(msg), 0, 0, 0, win.PM_REMOVE):
		#win.TranslateMessage(win.byref(msg))
		#win.DispatchMessage(win.byref(msg))
		if msg.message == win.WM_KEYDOWN and msg.wParam == win.VK_ESCAPE or need_to_exit: break

print("Please wait while saving Tracker memory... ", end='',  flush=True)
fsdkTracker.SaveToFile(trackerMemoryFile)
win.ShowWindow(hwnd, win.SW_HIDE)

img.Free()
fsdkTracker.Free()
camera.Close()

FSDK.FinalizeCapturing()

FSDK.Finalize()




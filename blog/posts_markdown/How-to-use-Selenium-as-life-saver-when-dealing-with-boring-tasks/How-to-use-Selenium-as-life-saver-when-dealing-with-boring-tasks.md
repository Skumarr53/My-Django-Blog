

If you are a developer then probably you do not need an intro to selenium. Selenium is a powerful tool built to interact with the webserver for processing requests in a programmatic way. It is used in automating a wide variety of tasks involving interaction with the remote web server. In this article, I will try to demonstrate its powerful usage through a simple example.

Let's consider the task of automating text extraction from a sample of scanned images, termed as Optical Character Recognition (OCR), using an online service. The following steps are involved in this process.

1. Uploading an image from local storage.
2. Initiating OCR extraction process
3. Wait until the text extraction is completed
4. Locate the text element and retrieve
5. write it in a txt file

I am using the [newocr](https://www.newocr.com/) online OCR service for task demonstration. As we go through the code step-by-step I will explain what is being done. The code is written in python however readers without python knowledge can understand the concept discussed here. I have picked a sample scanned images. Let's take a look at the sample images.

<img class="pg rf s t u ip ai iz" width="1093" height="633" srcset="https://miro.medium.com/max/552/1*xtvoBHq0z0MODlE-MVPbbw.png 276w, https://miro.medium.com/max/1104/1*xtvoBHq0z0MODlE-MVPbbw.png 552w, https://miro.medium.com/max/1280/1*xtvoBHq0z0MODlE-MVPbbw.png 640w, https://miro.medium.com/max/1400/1*xtvoBHq0z0MODlE-MVPbbw.png 700w" sizes="700px" role="presentation" src="https://miro.medium.com/max/1202/1*xtvoBHq0z0MODlE-MVPbbw.png">



## Importing required libraries

``` python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
```
* **webdriver** - Selenium driver class object that interacts with the server
* **WebDriverWait** - function for pausing execution for a while
* **expected_conditions** - for passing on waiting condition
* **TimeoutException** - For handling error due to server response delay
* **By** - for specifying element type to look for
* **ChromeDriverManager** - for launching Chrome version of browser

``` python
import glob 

files = glob.glob('*jpeg') 

print(files) 

dr = webdriver.Chrome(executable_path=r”C:\Program Files
(x86)\Google\Chrome\chromedriver.exe”);

dr.get('https://www.newocr.com/')
```
glob.glob list all the files with filenames that end with '.jpeg' (jpeg images) in the working directory. Also, you should see a Chrome browser getting launched automatically and land up on Newocr homepage.

*Note* : If chromedriver.exe is not available in the executable_path then you will encounter **'WebDriverException'** which means either driver stored is somewhere else or driver is absent. If the chromedriver.exe is absent download it and specify the full path of the location.

## Locate the Element tags

For each of the actions, we want selenium to perform on the element we need to provide the corresponding element path. The element path is the thing that points to a given tag in the HTML doc. The idea behind for doing this is we ask Selenium to go to tag at the given location and perform the specified action on it. Follow the steps shown below to get the element path.

<img class="in io s t u ip ai iz" width="1920" height="1080" srcset="https://miro.medium.com/max/552/1*S5jPgid4XdSVunG55TarSg.gif 276w, https://miro.medium.com/max/1104/1*S5jPgid4XdSVunG55TarSg.gif 552w, https://miro.medium.com/max/1280/1*S5jPgid4XdSVunG55TarSg.gif 640w, https://miro.medium.com/max/1456/1*S5jPgid4XdSVunG55TarSg.gif 728w, https://miro.medium.com/max/1632/1*S5jPgid4XdSVunG55TarSg.gif 816w, https://miro.medium.com/max/1808/1*S5jPgid4XdSVunG55TarSg.gif 904w, https://miro.medium.com/max/1984/1*S5jPgid4XdSVunG55TarSg.gif 992w, https://miro.medium.com/max/2000/1*S5jPgid4XdSVunG55TarSg.gif 1000w" sizes="1000px" role="presentation">


There are many ways by which you can locate elements, 'CCS selector' is one of them. Once, you do the above steps CSS selector of the element gets copied into the clipboard. Then use this selector to locate the element. Below is the code snippet that does text extraction from the images.

``` python
dr.find_element_by_css_selector('#userfile').send_keys(os.path.join(os.getcwd(),'Sample_1.jpeg'))

dr.find_element_by_css_selector('#preview').click()

WebDriverWait(dr,25).until(cond.visibility_of_element_located((By.CSS_SELECTOR,'#ocr')))

dr.find_element_by_css_selector('#ocr').click()
WebDriverWait(dr,25).until(cond.visibility_of_element_located((By.CSS_SELECTOR,'#ocr-result')))

txt = dr.find_element_by_css_selector('#ocr-result').get_attribute('value')
```

The above code snippet does the following things:
1. Locate the ‘Choose file’ button and sends the full path of the image file
2. Find the ‘Preview’ button and performs a click action triggering the uploading
process.
3. Waits until the ‘#ocr’ element appears which means uploading process is
completed but not more than 25 secs.
4. Once the element ‘#ocr’ appears performs a click action triggering the text
extraction process.
5. Waits until extraction gets completed.
6. Locates the retrieved text element and then copy the result and stores in variable
‘txt’.

Let’s put it into action.

<img class="in io s t u ip ai iz" width="1920" height="1080" srcset="https://miro.medium.com/max/552/1*yGe0WXHw-KFPOomsB3uxDw.gif 276w, https://miro.medium.com/max/1104/1*yGe0WXHw-KFPOomsB3uxDw.gif 552w, https://miro.medium.com/max/1280/1*yGe0WXHw-KFPOomsB3uxDw.gif 640w, https://miro.medium.com/max/1456/1*yGe0WXHw-KFPOomsB3uxDw.gif 728w, https://miro.medium.com/max/1632/1*yGe0WXHw-KFPOomsB3uxDw.gif 816w, https://miro.medium.com/max/1808/1*yGe0WXHw-KFPOomsB3uxDw.gif 904w, https://miro.medium.com/max/1984/1*yGe0WXHw-KFPOomsB3uxDw.gif 992w, https://miro.medium.com/max/2000/1*yGe0WXHw-KFPOomsB3uxDw.gif 1000w" sizes="1000px" role="presentation">

You may be wondering if doing the process manually is easier than programming why to code it. Imagine yourself in a situation where you have to process 100’s of images to extract text out of them which is a cumbersome process. In this case, Selenium could be a life-saver. Selenium makes your machine do the job while you are chatting with your colleagues at the office cafeteria, sipping coffee. Let’s see how it’s done.

``` python
for i in files:
    dr.find_element_by_css_selector('#userfile').send_keys(os.path.join(os.getcwd(),i))
    dr.find_element_by_css_selector('#preview').click()
    WebDriverWait(dr,25).until(cond.visibility_of_element_located((By.CSS_SELECTOR,'#ocr')))
    dr.find_element_by_css_selector('#ocr').click()
    WebDriverWait(dr,25).until(cond.visibility_of_element_located((By.CSS_SELECTOR,'#ocr-result')))
    txt = txt + "\n\n\nOutput from the "+i+" :\n\n"+ dr.find_element_by_css_selector('#ocr-result').get_attribute('value')
    dr.find_element_by_css_selector('#form-ocr > div.form-actions.span18 > button:nth-child(3)').click() 
print(txt)
```

The code loops through every image and applies the operations discussed earlier on it. The code snippet ran on sample images produces the below result.


The output from the Sample_1.jpeg :

>*In 1830 there were Dut twenty-three
miles of railroad in operation in the
United States, and in that year Ken-
tucky took the initial step in the work
weat of the Alleghanies. An Act to
incorporate the Lexington & Ohio
Railway Company was approved by
Gov. Metcalf, January 27, 1830.. {t
provided for the construction and re.*

The output from the Sample_2.jpeg :

>*When you skim and scan, you need to cover
everything, even titles, subtitles, side features, and
visuals. That bit of information you need may not be
tidily packaged in a paragraph, so you need to check
the entire page--not just the main body of the text,
there are also many visual clues that help you to
find information. Heads and subheads break up the
text and identify the content of each part. Where
key terms are introduced and defined, they appear
in boldface type. Graphs and charts have titles
and/or captions that tell you what they are about.
These clues will help you to find information. . . but
only if you use them.*


The output from the Sample_3.jpeg :

>*irks Scan*<br><br>
>*Tris scanning meusures the iris pattern in the cotored part of the eye,
although the iris color has nothing to do with the biornetric. tris
patterns are formed randomly. As a result, the iris patterns in your
left and right eyes are different, and so are the iris patterns of identi-
cal twins, Iris scan templates ure typically around 256 bytes. bis
scanning can be used quickly for both identification and verification
applications because of its large number of degrees of freedom, Cur-
Tent pilot programs and applications include ATMs (“Eye-TMs"),
grocery stores (for checking out), and the Charlotte/Douglas Inter-
national Airport (physical access}. During the Winter Otympics in
Nagano, Japan, an iris scanning identification system controlled
access to the rifles used in the biathlon*

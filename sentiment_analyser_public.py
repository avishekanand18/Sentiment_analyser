from tkinter import *
import tweepy
from textblob import TextBlob
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class senti_analyser:
    def __init__(self):
        self.consumer_key =""
        self.consumer_secret = ""

        self.acces_token = ""
        self.acces_token_secret = ""

        self.auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
        self.auth.set_access_token(self.acces_token,self.acces_token_secret)

        self.api = tweepy.API(self.auth)



        #Setting GUI 
        self.root = Tk()
        self.root.title("Sentiment Analyser")
        #self.root.geometry('800x300')    
        self.canvas1 = Canvas(self.root, width = 640, height = 350)
        self.canvas1.configure(background="floral white") #Changing the Background Color
        
        self.canvas1.pack()
        self.lb0= Label(self.canvas1,text="sentiment analyzer ",bg="deep skyblue",fg="ghost white")
        self.lb0.configure(font=("Constantia",22,"bold"))
        self.canvas1.create_window(330,30,window=self.lb0)

        #label
        self.lb1 = Label(self.root,text ="Enter Text to Search :",bg="floral white",fg="grey1")
        self.canvas1.create_window(180,90,window=self.lb1)

        self.lb2 = Label(self.root,text ="Enter no. of Tweets to Analyse :",bg="floral white",fg="grey1")
        self.canvas1.create_window(470,90,window=self.lb2)

        #search_Box
        self.txt=Entry(self.root,width=30)
        self.canvas1.create_window(180,120,window=self.txt)

        self.txt2=Entry(self.root,width=10)
        self.canvas1.create_window(470,120,window=self.txt2)

        self.lb3 = Label(self.root,text = "  ",bg="floral white")
        self.canvas1.create_window(350,200,window=self.lb3)

        #action performed when button is clicked
        def btn_clicked():
            self.search_txt = self.txt.get()
            self.no_of_tweets = self.txt2.get()
            self.public_tweets = self.api.search(q=self.search_txt, count=self.no_of_tweets)
            #self.lbl.configure(text=self.fr)
        

            #initailizing sum of sentiments to zero                                                  
            self.s=0

            #initailizing count of sentiments to zero
            self.count=0

            self.positive_tweet=0

            self.negative_tweet=0

            self.neutral_tweet=0

            #traverse through each tweet
            for tweet in self.public_tweets:
                #performing analysis on each tweet using textblob
                analysis = TextBlob(tweet.text)
                x=analysis.sentiment.polarity
                #print(x)

                #cases where sentiment analysis comes to zero are not considered
                #counts total positive, negative and neutral tweets
                if x > 0:
                    self.positive_tweet=self.positive_tweet+1
                    self.s=self.s+(x)
                    self.count=self.count+1
                elif x < 0:
                    self.negative_tweet=self.negative_tweet+1
                    self.s=self.s+(x)
                    self.count=self.count+1
                else:
                    self.neutral_tweet=self.neutral_tweet+1
                    
            #to prevent zero division error
            if self.count == 0:
                self.lbl.configure(text="Failed to Analyse Data! Retry")
            else:
                
                result = ((self.s)/self.count)

                if result>0:
                    fr = "The overall sentiment is 'Positive' and Positivity Rate is {:0.1f} %".format(result*100)
                elif result<0:
                    fr = "The overall sentiment is 'Negative' and Negativity Rate is {:0.1f} %".format(result*100)
                else:
                    fr = "The overall sentiment is 'Neutral' "
            
                
                self.lb3.configure(text=fr)
                #self.lb2.configure(text='')
                
                self.figure1 = Figure(figsize=(4.2,3), dpi=100) 
                self.subplot1 = self.figure1.add_subplot(111) 
                self.clabels = 'Positive Tweets', 'Negative Tweets', 'Neutral Tweets' 
                self.pieSizes = [float(self.positive_tweet),float(self.negative_tweet),float(self.neutral_tweet)]
                #self.my_colors = ['lightblue','lightsteelblue','silver']
                self.my_colors = ['green','red','silver']
                self.explode = (0.0, 0.0, 0.0)  
                self.subplot1.pie(self.pieSizes, colors=self.my_colors, explode=self.explode, labels=self.clabels, autopct='%1.1f%%', shadow=True) 
                #self.subplot2.axis('equal')  
                self.pie1 = FigureCanvasTkAgg(self.figure1, self.root)
                self.pie1.get_tk_widget().pack()
            
        self.btn=Button(self.root,text="Click to get Result",command=btn_clicked)
        self.canvas1.create_window(350, 170,window=self.btn)
        
        self.root.mainloop()


obj=senti_analyser()
    


# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds


def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def _init_(self,guid,title,subject,summary,link):
        self.guid=guid
        self.title=title
        self.subject=subject
        self.summary=summary
        self.link=link
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_subject(self):
        return self.subject
    def get_summary(self):
        return self.summary
    def get_link(self):
        return self.link
#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5
class WordTrigger(Trigger):
    def __init__(self,word):
        self.word=word
    def evaluate(self,story):
        Trigger.evaluate(self,story)

    def is_word_in(self,text):
        textlist = text.split(' ')
        for punc in string.punctuation:
            for i in textlist:
                if punc in i:
                    textlist.extend(i.split(punc))
                    textlist.remove(i)
        
        if self.word in textlist:
            return True
        else:
            return False
    def __str__(self):
        return self.word

class TitleTrigger(WordTrigger):
    def __init__(self,word):
        self.word = word
    def evaluate(self,story):
        myTitle = story.myTitle.lower()
        secondTitle = WordTrigger.is_word_in(self,myTitle)
        return secondTitle

class SubjectTrigger(WordTrigger):
    def __init__(self,word):
        self.word = word
    def evaluate(self,story):
        mySubject = story.mySubject.lower()
        secondSubject = WordTrigger.is_word_in(self,mySubject)
        return secondSubject

class SummaryTrigger(WordTrigger):
    def __init__(self,word):
        self.word = word
    def evaluate(self,story):
        mySummary = story.mySummary.lower()
        secondSummary = WordTrigger.is_word_in(self,mySummary)
        return secondSummary


class NotTrigger(Trigger):
    def __init__(self,Trigger):
        self.Trigger = Trigger
    def evaluate(self,story):
        return not self.Trigger.evaluate(story)


class AndTrigger(Trigger):
    def __init__(self,Trigger1,Trigger2):
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2
    def evaluate(self,story):
        if (((self.Trigger1.evaluate(story))== True) and (self.Trigger2.evaluate(story))):
            return True
        else:
            return False


class OrTrigger(Trigger):
    def __init__(self,Trigger1,Trigger2):
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2
    def evaluate(self,story):
        if (((self.Trigger1.evaluate(story))== True) or (self.Trigger2.evaluate(story))):
            return True
        else:
            return False
class PhraseTrigger(Trigger):
    #take in a string
    def __init__(self, phrase):
        self.phrase = phrase

    #is_phrase_in will check if that string is anywhere in the string 'text'
    def is_phrase_in(self, text):
        if self.phrase in text:
            return True
        else:
            return False

    #check title, subject, AND summary for our phrase
    def evaluate(self, story):
        return self.is_phrase_in(story.title) or self.is_phrase_in(story.subject) or self.is_phrase_in(story.summary)

def filter_stories(stories, triggerlist):
    #we want a list of stories; initiate an empty list
    filtered_stories = []
    #check each story against each trigger
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) == True:
                filtered_stories.append(story)
                #if the story has fired one trigger, we don't need to check the rest
                break
    return filtered_stories


# TODO: WordTrigger
# TODO: TitleTrigger
# TODO: SubjectTrigger
# TODO: SummaryTrigger


# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
# TODO: AndTrigger
# TODO: OrTrigger


# Phrase Trigger
# Question 9

# TODO: PhraseTrigger


#======================
# Part 3
# Filtering
#======================

#def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    return stories

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    #the list to be returned
    triggerlist = []
    #a dictionary of all triggers created
    allTriggers = {}
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        else:
            #keys will be our list of words in the line
            keys = line.split(' ')
            #any line starting with ADD adds the following n triggers to the list
            if keys[0] == 'ADD':
                for i in (1, len(keys)-1):
                    triggerlist.append(allTriggers[keys[i]])
            else:
                #title, subject, summary triggers built with one argument
                if keys[1] == 'TITLE':
                    trigger = TitleTrigger(keys[2])
                elif keys[1] == 'SUBJECT':
                    trigger = SubjectTrigger(keys[2])
                elif keys[1] == 'SUMMARY':
                    trigger = SummaryTrigger(keys[2])
                #not, and, or triggers take triggers as arguments
                elif keys[1] == 'NOT':
                    trigger = NotTrigger(allTriggers[keys[2]])
                elif keys[1] == 'AND':
                    trigger = AndTrigger(allTriggers[keys[2]], allTriggers[keys[3]])
                elif keys[1] == 'OR':
                    trigger = OrTrigger(allTriggers[keys[2]], allTriggers[keys[3]])
                elif keys[1] == 'PHRASE':
                    phrase = ''
                    #take however many words are listed
                    for i in (2, len(keys)-1):
                        #concatenate them to make a phrase
                        phrase = phrase + ' ' + keys[i]
                    trigger = PhraseTrigger(phrase)
                #make a dictionary entry for {trigger's name:trigger}
                allTriggers[keys[0]] = trigger
        lines.append(line)
    return triggerlist

    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    
import threading

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
##    t1 = SubjectTrigger("Obama")
##    t2 = SummaryTrigger("MIT")
##    t3 = PhraseTrigger("Supreme Court")
##    t4 = OrTrigger(t2, t3)
##    triggerlist = [t1, t4]
    
    # After implementing readTriggerConfig, uncomment this line
    #get triggers from a text file
    triggerlist = readTriggerConfig("triggers.txt")
    print triggerlist

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    tmain = threading.Thread(None, main_thread, None, (p,))
    tmain.start()
    p.start()





from Bases.BaseObjects import BaseObject
from Tools import Images
import pygame


class BackgroundImage(BaseObject):
    """
   Class that creates background image object and blits to screen
    """
    def __init__(self, il, x=0, y=0):
        BaseObject.__init__(self, il, x=x, y=y)

        self.width = 1000
        self.height = 955
        self.background = il.load_image(Images.ImageEnum.TitleBackground)
        self.resized_background = pygame.transform.scale(self.background,(self.width, self.height))

    def render(self, canvas):
        canvas.blit(self.resized_background, (self.x, self.y))


class OptionsScreenMessage(BaseObject):

    # Displays a header for the page

    def __init__(self, il, x = 230, y = 120):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = pygame.font.Font("Fonts/freesansbold.ttf", 120)
        self.options = self.font.render("Settings", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.options, (self.x, self.y))


class ResolutionSetting(BaseObject):
    
    # Displays resolution indicating the dropdown's purpose

    def __init__(self, il, x = 10, y = 350):
        BaseObject.__init__(self, il, x = x, y = y)

        self.font = pygame.font.Font("Fonts/OpenSans-Light.ttf", 60)
        self.resolution_message = self.font.render("Resolution: ", True, (255, 255, 255))
    
    def render(self, canvas):
        canvas.blit(self.resolution_message, (self.x, self.y))


class DropDownBox(BaseObject):

    # Creates a drop down box to switch the resolution

    def __init__(self, il, x = 375, y = 375):
        BaseObject.__init__(self, il, x = x, y = y)

        # Rectangle dimensions and color
        self.width = 250
        self.height = 40
        self.rgb = 255
        self.resWide = 1000
        self.resHeight = 955
        
        # Used to track if dropdown box is open or not
        self.active = False

        # Font for dropdown options
        self.font = pygame.font.Font("Fonts/OpenSans-Light.ttf", 35)
        
        # Dropdown option 1
        self.res1 = "1000 x 955"
        self.res1Display = self.font.render(self.res1, True, (0, 0, 0))
        self.res1x = x + 10
        self.res1y = y + 40

        # Dropdown option 2
        self.res2 = "1100 x 955"
        self.res2Display = self.font.render(self.res2, True, (0, 0, 0))
        self.res2x = x + 10
        self.res2y = y + 80

        # Dropdown option 3
        self.res3 = "1200 x 955"
        self.res3Display = self.font.render(self.res3, True, (0, 0, 0))
        self.res3x = x + 10
        self.res3y = y + 120

        # Active display
        self.activeDisplay = self.res1Display
        self.activeDisplayX = self.x + 10
        self.activeDisplayY = self.y - 5

        #Screen
        self.screen = [1000, 955]


    def handle_input(self, oh, events, pressed_keys):
        for event in events:
            location = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and self.active == False:
                # User clicks on the display
                if 375 < location[0] < 625 and 375 < location[1] < 415:
                    # Expand drop down box to larger size to accomodate all options
                    self.active = True
                    self.width = 250
                    self.height = 160  # space for 20 pxl between each dropdown option
                    self.rgb = 169
            elif event.type == pygame.MOUSEBUTTONDOWN and self.active == True:
                # User selects menu option 1
                if 375 < location[0] < 625 and 425 < location[1] < 455:
                    # Contract dropdown menu and display selection
                    self.active = False
                    self.width = 250
                    self.height = 40
                    self.rgb = 255
                    self.resWide = 1000
                    self.resHeight = 955
                    self.activeDisplay = self.res1Display
                elif 375 < location[0] < 625 and 465 < location[1] < 495:
                    self.active = False
                    self.width = 250
                    self.height = 40
                    self.rgb = 255
                    self.resWide = 1100
                    self.resHeight = 955
                    self.activeDisplay = self.res2Display
                elif 375 < location[0] < 625 and 505 < location[1] < 535:
                    self.active = False
                    self.width = 250
                    self.height = 40
                    self.rgb = 255
                    self.resWide = 1200
                    self.resHeight = 955
                    self.activeDisplay = self.res3Display
                else:
                    self.active = False
                    self.width = 250
                    self.height = 40
                    self.rgb = 255
    
    # Highlighting on dropdown options
    def update(self, oh):
        location = pygame.mouse.get_pos()
        if self.active == True:
            if 375 < location[0] < 625 and 425 < location[1] < 455:
                self.res1Display = self.font.render(self.res1, True, (255, 0, 0))
                self.res2Display = self.font.render(self.res2, True, (0, 0, 0))
                self.res3Display = self.font.render(self.res3, True, (0, 0, 0))
            elif 375 < location[0] < 625 and 465 < location[1] < 495:
                self.res1Display = self.font.render(self.res1, True, (0, 0, 0))
                self.res2Display = self.font.render(self.res2, True, (255, 0, 0))
                self.res3Display = self.font.render(self.res3, True, (0, 0, 0))
            elif 375 < location[0] < 625 and 505 < location[1] < 535:
                self.res1Display = self.font.render(self.res1, True, (0, 0, 0))
                self.res2Display = self.font.render(self.res2, True, (0, 0, 0))
                self.res3Display = self.font.render(self.res3, True, (255, 0, 0))

    def render(self, canvas):
        if self.active == False:
            pygame.draw.rect(canvas, (self.rgb, self.rgb, self.rgb), pygame.Rect(self.x, self.y, self.width, self.height))
            canvas.blit(self.activeDisplay, (self.activeDisplayX, self.activeDisplayY))
        elif self.active == True:
            pygame.draw.rect(canvas, (self.rgb, self.rgb, self.rgb), pygame.Rect(self.x, self.y, self.width, self.height))
            canvas.blit(self.res1Display, (self.res1x, self.res1y))
            canvas.blit(self.res2Display, (self.res2x, self.res2y))
            canvas.blit(self.res3Display, (self.res3x, self.res3y))

class ApplyButton(BaseObject):

    # User hits button to apply setting changes

    def __init__(self, il, x=450, y=700):
        BaseObject.__init__(self, il, x=x, y=y)

        # Button characteristics
        self.width = 100
        self.height = 40
        self.rgb = 255

        # Apply text written on button
        self.font = pygame.font.Font("Fonts/OpenSans-Light.ttf", 30)
        self.applyText = self.font.render("Apply", True, (0, 0, 0))
        self.applyTextX = x + 10
        self.applyTextY = y - 5

    def render(self, canvas):
        pygame.draw.rect(canvas, (self.rgb, self.rgb, self.rgb), pygame.Rect(self.x, self.y, self.width, self.height))
        canvas.blit(self.applyText, (self.applyTextX, self.applyTextY))


class ToMainScreen(BaseObject):
    """
    Returns users to the main screen
    """

    def __init__(self, il, x=23, y=900):
        BaseObject.__init__(self, il, x=x, y=y)

        self.font = pygame.font.Font("Fonts/OpenSans-Light.ttf", 30)
        self.start_button = self.font.render("Return to Main Menu", True, (255, 255, 255))

    def update(self, oh):
        """ Changes text color from white to red"""
        location = pygame.mouse.get_pos()
        button_coordinates = 26 < location[0] < 307 and 912 < location[1] < 934
        # if mouse is over to main screen button, color is changed to red
        if button_coordinates:
            self.start_button = self.font.render("Return to Main Menu", True, (166, 31, 36))
        else:
            self.start_button = self.font.render("Return to Main Menu", True, (255, 255, 255))

    def render(self, canvas):
        canvas.blit(self.start_button, (self.x, self.y))
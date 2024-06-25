import pygame, random, time

W = 1080
H = 720

class Game:
    def __init__(self):
        self.chapters = []
        self.currentMenu = None
        self.font = pygame.font.Font(None, 30)
        self.page = 0
        self.cards = []
        self.card_number = 0
        self.question = True
        self.createMenu("main")

    def getChapterText(self):
        fp = open("C:/Users/natha/Documents/Coding Projects/comptia_aplus/chapters.txt")
        self.chaptersText = []
        line_num = 0
        for line in fp:
            line_num += 1
            # Import text
            try:
                self.chaptersText.append(line.strip("\n"))
            except ValueError:
                print(f"error loading \"{line}\", line number:{line_num}")
            
        fp.close()

    def createMenu(self, menu:str):
        self.buttons = []
        self.text = []
        self.text_rects = []
        self.currentMenu = menu
        if menu == "main":
            self.createMain()
        if menu == "all_cards":
            self.cards = getData()
            self.startCards()
        if menu == "multi":
            self.createSelection()
        if menu == "test":
            self.createPickTest()

    def createMain(self):
            # All Chapters
            self.buttons.append((200, 100, 680, 140, self.createMenu, "all_cards"))
            self.text.append(self.font.render("All Chapters", True, "black"))
            self.text_rects.append(self.text[0].get_rect(center=(W/2, 170)))

            # Multi-Select
            self.buttons.append((200, 290, 680, 140, self.createMenu, "multi"))
            self.text.append(self.font.render("Select Sections", True, "black"))
            self.text_rects.append(self.text[1].get_rect(center=(W/2, 360)))

            # By Test
            self.buttons.append((200, 480, 680, 140, self.createMenu, "test"))
            self.text.append(self.font.render("Select Test", True, "black"))
            self.text_rects.append(self.text[2].get_rect(center=(W/2, 550)))

            self.mainMenu()

    def mainMenu(self):
        screen.fill("purple")
        for r in self.buttons:
            dropShadow(r[0:4])
            pygame.draw.rect(screen, "white", r[0:4], 0, 20, 20, 20, 20)
        for t, r in zip(self.text, self.text_rects):
            screen.blit(t, r)
    
    def createSelection(self):
        self.getChapterText()
        self.buttons = []
        if self.page != 3:
            for i in range(3):
                for j in range(3):
                    self.buttons.append((50 + j*340, 50 + i*200, 300, 150, self.addChapter, ((i*3)+j+1) + self.page * 9))
                    self.text_rects.append((60 + j*340, 60 + i*200, 280, 130))
        else:
            self.buttons.append((50, 50, 300, 150, self.addChapter, 28))
            self.text_rects.append((60, 60, 280, 130))

        self.createArrows()
        self.createStartButton()
        self.drawSelection()
    
    def drawSelection(self):
        screen.fill("purple")
        for i in range(len(self.buttons)-3):
            dropShadow(self.buttons[i][0:4])
            pygame.draw.rect(screen, "green" if self.buttons[i][5] in self.chapters else "white", self.buttons[i][0:4], 0, 20)
            drawText(screen, self.chaptersText[self.buttons[i][5]-1], "black", self.text_rects[i], self.font)
        self.drawArrows()
        self.drawStartButton()
    
    def addChapter(self, number):
        if number not in self.chapters:
            self.chapters.append(number)
        else:
            self.chapters.remove(number)
        self.drawSelection()

    def createArrows(self):
        self.buttons.append((300, 640, 50, 80, self.changePage, -1))
        self.buttons.append((730, 640, 50, 80, self.changePage, 1))

    def drawArrows(self):
        pygame.draw.polygon(screen, "azure3", [(300, 660), (350, 640), (350, 680)])
        pygame.draw.polygon(screen, "azure3", [(780, 660), (730, 640), (730, 680)])

    def changePage(self, number):
        self.page += number
        self.page %= 4
        self.createSelection()
    
    def createStartButton(self):
        self.buttons.append((440, 620, 200, 80, self.startPressed, "multi"))

    def drawStartButton(self):
        pygame.draw.rect(screen, "azure3", (440, 620, 200, 80), 0, 15, 15, 15, 15)
        start = "Start"
        startText = self.font.render(start, True, "black")
        startText_rect = startText.get_rect(center=(W/2, 660))
        screen.blit(startText, startText_rect)
        
    def startPressed(self, mode = "multi"):
        if mode == "multi":
            self.cards = getData(self.chapters)
            self.startCards()
    
    def createPickTest(self):
        # Background
        self.buttons.append((200, 100, 680, 140, self.pickTest, "1100"))
        self.text.append(self.font.render("Background Information", True, "black"))
        self.text_rects.append(self.text[0].get_rect(center=(W/2, 170)))

        # 1101
        self.buttons.append((200, 290, 680, 140, self.pickTest, "1101"))
        self.text.append(self.font.render("1101", True, "black"))
        self.text_rects.append(self.text[1].get_rect(center=(W/2, 360)))

        # 1102
        self.buttons.append((200, 480, 680, 140, self.pickTest, "1102"))
        self.text.append(self.font.render("1102", True, "black"))
        self.text_rects.append(self.text[2].get_rect(center=(W/2, 550)))
        
        self.drawPickTest()

    def drawPickTest(self):
        screen.fill("purple")
        for r in self.buttons:
            dropShadow(r[0:4])
            pygame.draw.rect(screen, "white", r[0:4], 0, 20)
        for t, r in zip(self.text, self.text_rects):
            screen.blit(t, r)        

    def pickTest(self, test):
        self.cards = getData()
        useCards = []
        for card in self.cards:
            if card.test == test:
                useCards.append(card)
        self.cards = useCards
        self.startCards()

    def startCards(self):
        self.currentMenu = "cards"
        random.shuffle(self.cards)
        try:
            self.drawCard(self.cards[0].question, "white")
        except IndexError:
            self.outOfCards()

    def drawCard(self, text:str, color:str):
        text_rect = (150, 150, 780, 420)
        screen.fill("purple")
        dropShadow((100, 100, 880, 520))
        pygame.draw.rect(screen, color, (100, 100, 880, 520), 0, 20, 20, 20, 20)
        font = pygame.font.Font(None, 50)
        drawText(screen, text, "black", text_rect, font)
        self.cardsRemaining()

    def cardsRemaining(self):
        totalText_font = pygame.font.Font(None, 30)
        text = f'Card {self.card_number+1 if self.card_number+1 <= len(self.cards) else len(self.cards)} of {len(self.cards)}'
        totalText = totalText_font.render(text, True, "white")
        totalText_rect = totalText.get_rect(center=(W/2, 50))
        screen.blit(totalText, totalText_rect)

    def outOfCards(self):
        self.currentMenu = "end"
        self.buttons = []
        screen.fill("purple")
        endText = self.font.render("Out of cards", True, "White")
        endText_rect = endText.get_rect(center=(W/2, H/2))

        screen.blit(endText, endText_rect)

class Card:
    def __init__(self, question, answer, test, chapter):
        self.question = question
        self.answer = answer
        self.test = test
        self.chapter = chapter

def drawText(surface:pygame.Surface, text:str, color:str, rect:tuple, font:pygame.font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if text.find("!", 1, i) > 0:
            i = text.find("!", 1, i)
        elif i < len(text):
            i = text.rfind(" ", 0, i) + 1

        text = text.replace("!", "", 1)

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

def getData(sections:list = [i for i in range(1,29)]):
    fp = open("C:/Users/natha/Documents/Coding Projects/comptia_aplus/data.txt")
    cards = []
    line_num = 0
    use_section = False
    for line in fp:
        line_num += 1
        # Handle section headers
        if line.find("$") == 0:
            if int(line[1]) in sections:
                use_section = True
                c = int(line[1])
            elif int(line[1]) not in sections:
                use_section = False
            continue

        # Handle flash card data
        try:
            if use_section:
                q, a, t = line.strip("\n").split(":")
                cards.append(Card(q, a, t, c))
        except ValueError:
            print(f"error loading \"{line}\", line number:{line_num}")
        
    fp.close()
    return cards

def animate(frontColor:str, backColor:str):
    x_values = [100, 328, 415, 520, 415, 328, 100]
    colors = [frontColor for _ in range(4)]
    for _ in range(3): colors.append(backColor)

    for x, c in zip(x_values, colors):
        screen.fill("purple")
        cardRect = (x, 100, (W - (2*x)), 520)
        dropShadow(cardRect)
        pygame.draw.rect(screen, c, cardRect, 0, 20, 20, 20, 20)
        game.cardsRemaining()
        pygame.display.flip()
        time.sleep(1/50)

def dropShadow(rect:tuple):
    shadowSizes = [5 + 5*i for i in range(8)]
    shadow_surface = pygame.Surface((1080, 720), pygame.SRCALPHA)

    for size in shadowSizes:
        shadowRect = [rect[0] - size, rect[1] - size + 50, rect[2] + size*2, rect[3] + size*2 - 25]
        pygame.draw.rect(shadow_surface, pygame.Color(0,0,0,10), shadowRect, 0, 20, 20, 20, 20)
        screen.blit(shadow_surface, (0,0))

pygame.init()

pygame.display.set_caption("Flash Cards")
screen = pygame.display.set_mode((W, H))
running = True
clock = pygame.time.Clock()

random.seed()

game = Game()

pygame.display.flip()

while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if game.currentMenu == "cards":
                try:
                    if game.question:
                        animate("white", "azure2")
                        game.drawCard(game.cards[game.card_number].answer, "azure2")
                        game.question = False
                    else:
                        game.card_number += 1
                        animate("azure2", "white")
                        game.drawCard(game.cards[game.card_number].question, "white")
                        game.question = True
                except IndexError:
                    game.outOfCards()
            else:
                for button in game.buttons:
                    rect = pygame.Rect(*button[0:4])
                    if rect.collidepoint(event.pos):
                        button[4](button[5])
            pygame.display.flip()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = Game()
                pygame.display.flip()
    
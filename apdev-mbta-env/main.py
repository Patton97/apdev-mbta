import requests
import json

import apdev_mbta_api_wrapper

def runAPITest():
    params = apdev_mbta_api_wrapper.GetStopsParams()
    params.sort = 'name'
    params.routeTypes = [0,1]

    with requests.Session() as s:
        response = apdev_mbta_api_wrapper.getStops(s, params)

    resultsJsonObj = json.loads(response.content)
    results = apdev_mbta_api_wrapper.parseResultsJson(resultsJsonObj)

    for result in results:
        print(result.name)

def runPygameTest():
    import pygame

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        pygame.draw.circle(screen, "green", pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), 4)


        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

runPygameTest()
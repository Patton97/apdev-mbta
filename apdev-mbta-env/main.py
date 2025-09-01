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

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    # TODO: surely there's a better wayof doing this
    MAX_FPS = 60
    MAX_LED_PIN_ANIMATION_FRAME = MAX_FPS * 3
    currentAnimationFrame = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('black')

        if currentAnimationFrame > MAX_FPS * 2:
            colour = 'chartreuse'
            radius = 10
        else:
            colour = 'chartreuse4'
            radius = 8
        pygame.draw.circle(screen, colour, pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), radius)

        pygame.display.flip()

        currentAnimationFrame += 1
        if currentAnimationFrame == MAX_LED_PIN_ANIMATION_FRAME:
            currentAnimationFrame = 0
        clock.tick(MAX_FPS)

    pygame.quit()

runPygameTest()
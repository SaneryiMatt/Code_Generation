export const mockSocketResponse = (route, messages) => {
  route.fulfill({
    status: 101,
    webSocket: {
      onOpen: (ws) => {
        messages.forEach((msg, i) => {
          setTimeout(() => ws.send(JSON.stringify(msg)), i * 100)
        })
      }
    }
  })
}

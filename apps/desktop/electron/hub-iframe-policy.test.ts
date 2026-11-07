import { describe, expect, it } from 'vitest'

import { focusedFrameOrigin, HERMES_HUB_ORIGIN, isHermesHubClipboardWrite } from './hub-iframe-policy'

// The session handlers receive the TOP document's webContents; the embedded hub is a subframe.
const appWindow = { getURL: () => 'file:///opt/hermes/app/index.html' }
const pickerUrl = `${HERMES_HUB_ORIGIN}/docs/skills?embed=picker`

describe('focusedFrameOrigin', () => {
  it("judges the requesting frame, so the embedded hub's Copy is allowed", () => {
    expect(isHermesHubClipboardWrite(focusedFrameOrigin(appWindow, { requestingUrl: pickerUrl }))).toBe(true)
  })

  it('cannot see the hub from the top document alone', () => {
    expect(focusedFrameOrigin(appWindow)).toBe('null') // a file: URL's origin is opaque
    expect(isHermesHubClipboardWrite(focusedFrameOrigin(appWindow))).toBe(false)
  })

  it('denies any other requesting frame, including opaque and unparseable ones', () => {
    for (const requestingUrl of ['https://evil.example/', 'data:text/html,x', 'about:blank', 'not a url']) {
      expect(isHermesHubClipboardWrite(focusedFrameOrigin(appWindow, { requestingUrl }))).toBe(false)
    }
  })
})

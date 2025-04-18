test.describe('新增按钮功能', () => {
  test('复制按钮', async ({ page }) => {
    await page.goto('/result?code=test-code')
    await page.getByRole('button', { name: '复制代码' }).click()

    const clipboardText = await page.evaluate(() =>
      navigator.clipboard.readText()
    )
    expect(clipboardText).toContain('test-code')
  })

  test('下载按钮', async ({ page }) => {
    const downloadPromise = page.waitForEvent('download')
    await page.getByRole('button', { name: '下载' }).click()
    const download = await downloadPromise
    expect(download.suggestedFilename()).toBe('generated-code.ts')
  })
})

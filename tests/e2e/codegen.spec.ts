import { test, expect } from '@playwright/test'

test('模拟完整代码生成流程', async ({ page }) => {
  // 1. 访问页面
  await page.goto('/')

  // 2. 输入测试需求
  await page.locator('textarea').fill('创建学生管理系统')
  await page.getByRole('button', { name: '下一步 →' }).click()

  // 3. 手动触发前端状态更新（绕过WebSocket）
  await page.evaluate(() => {
    // 模拟代码生成状态
    window.$mockState = {
      progress: 30,
      code: '// 模拟生成的代码\nclass Student {}',
      currentModule: '实体层'
    }

    // 触发Vue组件更新（根据你的框架调整）
    if (window.$vueApp) {
      window.$vueApp.$store.commit('updateState', window.$mockState)
    }
  })

  // 4. 验证进度条更新
  await expect(page.locator('.progress-bar')).toHaveCSS('width', '30%', { timeout: 5000 })

  // 5. 模拟生成完成
  await page.evaluate(() => {
    window.$mockState.progress = 100
    window.$mockState.code = `// 完整代码
@Entity()
class Student {
  @PrimaryGeneratedColumn()
  id: number

  @Column()
  name: string
}`
  })

  // 6. 验证代码显示
  await expect(page.locator('pre code')).toContainText('@Entity()', { timeout: 5000 })

  // 7. 点击查看代码按钮
  await page.getByRole('button', { name: '查看代码 →' }).click()
  await expect(page.getByText('@PrimaryGeneratedColumn()')).toBeVisible()
})

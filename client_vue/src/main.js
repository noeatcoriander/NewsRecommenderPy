/**
 * vue3前端系统主配置文件
 * 负责初始化vue实例、配置全局路由，将应用挂载到html页面的dom元素上等
 */
//导入vue的createApp函数
import { createApp } from 'vue'
//导入根组件App.vue
import App from './App.vue'
//导入路由配置
import router from './router/mainRouter'
//导入状态管理库：pinia
import { createPinia } from 'pinia'

//导入element plus的ui组件及图标组件
import ElementPlus, { ElMessageBox } from 'element-plus'
import 'element-plus/dist/index.css'
import { zhCn } from "element-plus/es/locale/index"
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

//导入fortawesome字体图标样式文件
//element plus的图标量较少，故再使用fortawesome
//官网：https://fa6.dashgame.com/
import '@fortawesome/fontawesome-free/css/all.css'

//导入前端基础样式文件
import '@/style/css_public.css'

//创建vue应用实例，并指定根组件：App.vue
const app = createApp(App)

//注册路由插件
app.use(router)

//创建状态管理库pinia实例
const pinia = createPinia()
//注册pinia插件
app.use(pinia)

//注册element plus的ui组件
app.use(ElementPlus, {
  locale: zhCn //中文
})

//注册element plus的图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

//element plus的ElMessageBox.confirm消息弹框全局配置
//由于ElMessageBox.confirm消息弹框功能默认会隐藏网页滚动条，导致网页样式变化，以下配置用于取消隐藏网页滚动条
//confirm默认消息弹框方法
const originalConfirm = ElMessageBox.confirm
//重写confirm方法，添加取消隐藏网页滚动条，lockScroll: false
ElMessageBox.confirm = function (message, title, options = {}) {
  //合并配置
  const mergedOptions = {
    lockScroll: false,//取消隐藏网页滚动条
    ...options //其他默认配置
  }
  //调用默认方法并返回
  return originalConfirm(message, title, mergedOptions)
}

//将vue应用挂载到index.html页面的dom元素上
app.mount('#app')

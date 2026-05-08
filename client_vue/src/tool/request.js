/**
 * 自定义axios异步请求后端数据接口实例
 * axios用于请求后端数据接口
 */
import axios from 'axios'
import { ElMessage } from "element-plus"
import router from "@/router/mainRouter"
import { baseUrlGlobal, requestTimeGlobal } from "@/tool/public"
import { useUserStore } from "@/store/userStore"

//创建axios异步请求实例对象
const request = axios.create({
  baseURL: baseUrlGlobal, //后端数据接口地址前缀
  timeout: requestTimeGlobal //请求超时时间（毫秒）
})

/**
 * 配置axios的请求request、响应response拦截器
 * 当在vue组件中使用axios向后端发送数据请求时，先执行axios的request请求拦截器、后端接收请求并返回数据、
 * 再执行axios的response响应拦截器、最后到达vue组件方法
 */

//request请求拦截器
request.interceptors.request.use(config => {
  //设置数据传输格式和编码：json格式、utf-8编码
  config.headers['Content-Type'] = 'application/json;charset=utf-8'

  //在request请求头中添加token，用于身份认证
  let token = null
  if (config.url.startsWith('/user')) {
    //如果请求地址以/user开头，获取当前登录用户的token
    token = useUserStore().token || null
  }
  //在request请求头中添加token
  //在token字符串前添加'Bearer '特指是身份认证的token
  config.headers.Authorization = `Bearer ${token}`

  return config //返回配置后的config
}, error => {
  //捕获请求前的异常
  console.info(error)
  return Promise.reject(error) //返回异常
})

//response响应拦截器
request.interceptors.response.use(response => {
  //后端返回状态码正常，即后端数据处理正常

  //在响应头中获取token状态，判断token是否有效
  const tokenState = response.headers['token-status']
  if (tokenState === 'invalid') {//token无效
    if (response.config.url.startsWith('/user')) {
      //如果请求地址以/user开头，删除登录用户信息和token
      useUserStore().doRemove()
    }
  }

  //获取后端返回的数据
  let res = response.data
  if (typeof res === 'string') {
    //如果后端返回字符串数据，则转json格式
    res = res ? JSON.parse(res) : res
  }

  /**
   * axios的常用请求方式：get、post、put、delete
   * get用于数据查询请求、post用于数据添加请求、put用于数据修改请求、delete用于数据删除请求
   * 配置post、put、delete的统一响应处理：弹窗提示操作成功或操作失败
   */
    //获取response响应的配置对象
  const config = response.config
  //判断请求方式
  //skipGlobalCheck：临时配置变量，在vue组件中调用axios时可添加此配置
  //此配置会忽略response响应的统一处理，交由vue组件自行处理
  if (config.method !== 'get' && !config.skipGlobalCheck) {
    const message = res.message //获取后端返回的操作提示信息
    //判断后端返回的操作成功或者失败标记，success > 0：操作成功，success <= 0：操作失败
    if (res.success > 0) {
      ElMessage.success(message ? message : '操作成功！')
    } else {
      ElMessage.error(message ? message : '操作失败！')
    }
  }

  return res //返回响应的数据
}, async error => {
  //后端返回状态码异常，即后端数据处理异常
  //网页控制台输出异常信息
  console.info(error)

  //判断异常响应对象是否存在
  if (error.response) {
    const status = error.response.status //获取异常响应状态码
    const message = error.response.data.message //获取异常响应信息

    //异常响应状态码：401，token无效，身份认证失败，即用户未登录
    if (status === 401) {
      ElMessage.error(message ? message : '操作失败！请先登录！')
      //如果请求地址以/user开头
      if (error.config.url.startsWith('/user')) {
        //删除登录用户信息和token
        useUserStore().doRemove()
        //跳转到登录页面
        await router.replace("/login") //replace替换当前路由，不保留历史记录
      }

      //异常响应状态码：404，请求的后端地址不存在
    } else if (status === 404) {
      ElMessage.error('操作失败！请求地址不存在！')

      //异常响应状态码：405，请求方式不匹配，前端和后端的请求发送和接收方式必须一致：前端发送post请求，后端接收post请求
    } else if (status === 405) {
      ElMessage.error('操作失败！请求方法不支持！')

      //异常响应状态码：500，后端代码运行异常
    } else if (status === 500) {
      ElMessage.error('操作失败！系统异常！')

      //其他异常响应状态码
    } else {
      ElMessage.error('操作失败！服务端异常！')
    }
  } else {
    //当后端服务器没有启动或前端请求超时，error.response对象为空
    ElMessage.error('操作失败！服务端无响应或请求超时！')
  }

  return Promise.reject(error) //返回异常
})

export default request
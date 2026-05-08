/**
 * 基础工具方法
 */
import { baseUploadUrlGlobal, uploadImageSizeLimitGlobal } from './public'
import { ElMessage, ElMessageBox } from "element-plus"
import request from "@/tool/request"

//新闻内容图片url路径添加前缀函数
//新闻内容字符串中保存新闻图片：<img src="/files/新闻图片名称.jpg"/>
//在src前添加前缀路径：http://localhost:8080/files/新闻图片名称.jpg
export const handleNewsContent = (introduction) => {
  if (!introduction)
    return ''
  //添加url前缀
  return introduction.replace(/src="\/files\//g, `src="${baseUploadUrlGlobal}`)
}

//校验年龄范围
export const handleValidateAge = (rule, value, callback) => {
  const age = parseInt(value)
  if (age < 10 || age > 90) {
    callback(new Error('年龄范围不正确（10-90）'))
  } else {
    callback()
  }
}

//校验密码和确认密码是否相同
export const handleValidateConfpassword = (formModel) => {
  console.info()
  return (rule, value, callback) => {
    if (value !== formModel.password) {
      callback(new Error('两次密码不相同'))
    } else {
      callback()
    }
  }
}

//校验电话格式
export const handleValidateMobile = (rule, value, callback) => {
  if (!/^1[3-9]\d{9}$/.test(value)) {
    callback(new Error('电话格式不正确'))
  } else {
    callback()
  }
}

//图片上传前校验上传图片的格式、大小
export const handleUploadImageBefore = (file) => {
  const isImage = file.type.startsWith('image/') //判断上传图片类型
  const isSizeLimit = file.size / 1024 / 1024 <= uploadImageSizeLimitGlobal //判断上传图片大小
  if (!isImage) {
    ElMessage.error('上传图片格式错误！')
    return false
  }
  if (!isSizeLimit) {
    ElMessage.error(`上传图片大小已超过${uploadImageSizeLimitGlobal}MB!`)
    return false
  }
  return true
}

/**
 * 批量删除
 * @param selectIds 选中的数据id，数组
 * @param deleteUrl 删除url请求地址
 * @param callbackFun 回调函数
 */
export const handleDeleteBatch = (selectIds, deleteUrl, callbackFun) => {
  if (selectIds.length === 0) {
    ElMessage.warning('请至少选择一条数据！')
    return
  }
  ElMessageBox.confirm('确认删除？', '确认删除', { type: 'warning' }).then(() => {
    //删除
    request.delete(deleteUrl, { data: selectIds }).then((res) => {
      if (callbackFun) {
        callbackFun() //回调函数
      }
    })
  }).catch(() => {
    //取消删除
  })
}
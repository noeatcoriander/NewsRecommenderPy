/**
 * 系统常量工具文件
 */

//系统名称
export const projectNameGlobal = '个性化新闻推荐系统'

//后端数据接口基础地址
export const baseUrl = 'http://localhost:8000'

//后端数据接口地址前缀，请求后端数据接口前统一添加/api，为了区分前端路由地址与后端api数据接口地址
export const baseUrlGlobal = baseUrl + '/api/'

//后端上传文件基础地址
export const baseUploadUrlGlobal = baseUrl + '/files/'

//axios异步请求后端数据超时时间（单位：毫秒），20000：20秒
export const requestTimeGlobal = 20000

//element plus分页ui组件，每页条数数组
export const pageSizesGlobal = [6, 12, 18, 24]

//element plus分页ui组件，默认每页条数
export const pageSizeGlobal = pageSizesGlobal[1]

//图片上传，允许上传的图片类型
export const uploadImageTypesGlobal = 'image/jpg,image/jpeg,image/png,image/bmp,image/webp'

//图片上传，允许上传的图片类型提示信息
export const uploadImageTypesTipGlobal = 'jpg、jpeg、png、bmp、webp'

//图片上传，允许上传的图片大小，单位：MB
export const uploadImageSizeLimitGlobal = 10

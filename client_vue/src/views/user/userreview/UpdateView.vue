<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">修改评论</div>
    </div>
    <div class="main-content">
      <el-row :gutter="30">
        <el-col :span="5">
          <Menu/>
        </el-col>
        <el-col :span="19">
          <div class="content-right">
            <div>
              <el-form ref="formRef" :rules="data.formRules" :model="data.formModel"
                       label-width="25%" style="max-width: 90%" label-suffix="：">
                <el-row :gutter="10">
                  <el-col v-if="data.formModel.news?.photo" :span="5">
                    <el-form-item label-width="10%" style="margin-top: 10px;">
                      <el-image :src="baseUploadUrlGlobal+data.formModel.news?.photo" fit="fill"
                                style="width: 100%;"/>
                    </el-form-item>
                  </el-col>
                  <el-col v-else :span="5"></el-col>
                  <el-col :span="19">
                    <el-form-item label="新闻标题">
                      <router-link class="el-link text-break" :to="'/user/news/detail?newsid='+data.formModel.newsid">
                        {{ data.formModel.news?.title }}
                      </router-link>
                    </el-form-item>
                    <el-form-item label="评论内容" prop="introduction">
                      <el-input type="textarea" v-model.trim="data.formModel.introduction" :rows="8" maxlength="2000"/>
                    </el-form-item>
                  </el-col>
                </el-row>
                <div style="display: flex;justify-content: center;margin: 30px 0;">
                  <el-button type="warning" @click="doSubmit">提交</el-button>
                </div>
              </el-form>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import Menu from "@/components/user/Menu.vue"
import { reactive, ref } from 'vue'
import request from "@/tool/request"
import { useRoute, useRouter } from "vue-router"
import { baseUploadUrlGlobal } from "@/tool/public"

//获取全局路由器实例对象
const router = useRouter()
//获取当前路由实例对象
const route = useRoute()

//从路由地址的参数中获取评论id
const userreviewid = route.query.userreviewid || ''

//创建表单组件的引用实例对象，可调用表单的属性和方法
const formRef = ref()

//创建页面的响应式数据对象
const data = reactive({
  formModel: {}, //表单数据对象
  formRules: { //表单数据校验规则对象
    introduction: [
      { required: true, message: '请输入评论内容', trigger: 'blur' }
    ]
  }
})

//提交数据
const doSubmit = () => {
  //校验表单数据
  formRef.value.validate((valid) => {
    if (valid) {
      //提交数据
      request.post('/user/userreview/doUpdate', { ...data.formModel, userreviewid: userreviewid }).then(res => {
        if (res.success > 0) {//操作成功
          //跳转到查看评论页面
          router.push('/user/userreview/detail?userreviewid=' + userreviewid)
        }
      })
    }
  })
}

//加载数据
const loadData = () => {
  if (userreviewid) {
    //请求数据
    request.get('/user/userreview/detail?userreviewid=' + userreviewid).then(res => {
      data.formModel = res.userreview //评论数据
    })
  }
}

//加载数据
loadData()
</script>

<style scoped>
</style>
<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">个人信息</div>
    </div>
    <div class="main-content">
      <el-row :gutter="30">
        <el-col :span="5">
          <Menu/>
        </el-col>
        <el-col :span="19">
          <div class="content-right">
            <div>
              <el-form label-width="25%" style="max-width: 90%" label-suffix="：">
                <el-row :gutter="10">
                  <el-col :span="5">
                    <el-form-item label-width="10%" style="margin-top: 10px;">
                      <el-image :src="baseUploadUrlGlobal+data.formModel.avatar" fit="fill"
                                style="width: 100%;"/>
                    </el-form-item>
                  </el-col>
                  <el-col :span="19">
                    <el-form-item label="用户名">{{ data.formModel.loginname }}</el-form-item>
                    <el-form-item label="姓名">{{ data.formModel.realname }}</el-form-item>
                    <el-form-item label="电话">{{ data.formModel.mobile }}</el-form-item>
                    <el-form-item label="邮箱">{{ data.formModel.email }}</el-form-item>
                    <el-form-item label="性别">
                      {{ data.formModel.sex === 1 ? '男' : (data.formModel.sex === 2 ? '女' : '') }}
                    </el-form-item>
                    <el-form-item label="年龄">
                      {{ data.formModel.age ? data.formModel.age + '岁' : '' }}
                    </el-form-item>
                    <el-form-item label="个人简介">
                      <div class="text-break" style="line-height: normal">{{ data.formModel.introduction }}</div>
                    </el-form-item>
                    <el-form-item label="注册时间">{{ data.formModel.savedate }}</el-form-item>
                  </el-col>
                </el-row>
                <div style="display: flex;justify-content: center;margin: 30px 0;">
                  <el-button type="warning" @click="router.push('/user/user/update')">修改信息</el-button>
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                  <el-button type="info" @click="router.push('/user/user/updatePassword')">修改密码</el-button>
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
import { reactive } from 'vue'
import { baseUploadUrlGlobal } from "@/tool/public"
import request from "@/tool/request"
import { useRouter } from "vue-router"

//获取全局路由器实例对象
const router = useRouter()

//创建页面的响应式数据对象
const data = reactive({
  formModel: {} //表单数据对象
})

//获取用户信息函数
const loadData = () => {
  //请求数据
  request.get('/user/user/detail').then(res => {
    data.formModel = res.user //用户信息
  })
}

//加载数据
loadData()
</script>

<style scoped>

</style>
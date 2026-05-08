<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">修改密码</div>
    </div>
    <div class="main-content">
      <el-row :gutter="30">
        <el-col :span="5">
          <Menu/>
        </el-col>
        <el-col :span="19">
          <div class="content-right">
            <div>
              <el-form ref="formRef" :rules="data.formRules" :model="formModel" label-width="25%"
                       style="max-width: 90%" label-suffix="：">
                <el-row :gutter="10">
                  <el-col :span="5">
                    <el-form-item label-width="10%" style="margin-top: 10px;">
                      <el-image :src="baseUploadUrlGlobal+userStore.user?.avatar" fit="fill"
                                style="width: 100%;"/>
                    </el-form-item>
                  </el-col>
                  <el-col :span="19">
                    <el-form-item label="原密码" prop="oldPassword">
                      <el-input show-password v-model.trim="formModel.oldPassword" maxlength="30"/>
                    </el-form-item>
                    <el-form-item label="新密码" prop="password">
                      <el-input show-password v-model.trim="formModel.password" maxlength="30"/>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="confPassword">
                      <el-input show-password v-model.trim="formModel.confPassword" maxlength="30"/>
                    </el-form-item>
                  </el-col>
                </el-row>
                <div style="display: flex;justify-content: center;margin: 30px 0;">
                  <el-button type="warning" @click="doSubmit">提交</el-button>
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                  <el-button type="info" @click="router.push('/user/user/update')">修改信息</el-button>
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
import { useRouter } from "vue-router"
import { handleValidateConfpassword } from "@/tool/tool"
import { useUserStore } from "@/store/userStore"
import { baseUploadUrlGlobal } from "@/tool/public"

//获取全局路由器实例对象
const router = useRouter()
//获取当前登录用户的状态管理实例对象
const userStore = useUserStore()

//创建表单组件的引用实例对象，可调用表单的属性和方法
const formRef = ref()
//创建表单数据的响应式实例对象
const formModel = reactive({})

//创建页面的响应式数据对象
const data = reactive({
  formRules: { //表单校验规则
    oldPassword: [
      { required: true, message: '请输入原密码', trigger: 'blur' },
      { min: 5, message: '长度最少5位', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入新密码', trigger: 'blur' },
      { min: 5, message: '长度最少5位', trigger: 'blur' }
    ],
    confPassword: [
      { required: true, message: '请输入确认密码', trigger: 'blur' },
      { min: 5, message: '长度最少5位', trigger: 'blur' },
      { validator: handleValidateConfpassword(formModel), trigger: 'blur' } //密码和确认密码是否相同校验
    ]
  }
})

//保存数据
const doSubmit = () => {
  //表单数据校验
  formRef.value.validate((valid) => {
    if (valid) {
      //提交数据
      request.post('/user/user/doUpdatePassword', formModel).then(res => {
        if (res.success > 0) {//操作成功
          userStore.doRemove() //删除登录用户信息
          router.replace('/login') //跳转到登录页面
        }
      })
    }
  })
}
</script>

<style scoped>

</style>
<template>
  <div class="login-container">
    <div class="main-layout">
      <div class="main-content">
        <div class="main-login">
          <div class="login-title">
            <h5>
              <router-link to="/" class="el-link">
                {{ projectNameGlobal }}
              </router-link>
              <div style="font-size: 1.2rem;margin: 10px 0 0 0;color: #582F0E;font-weight: normal;">用户注册</div>
            </h5>
          </div>
          <div class="login-form">
            <el-form ref="formRef" :model="formModel" :rules="data.formRules" label-width="auto" size="large"
                     label-suffix="：">
              <el-form-item label="用户名" prop="loginname">
                <el-input v-model.trim="formModel.loginname" maxlength="30"/>
              </el-form-item>
              <el-form-item label="电话" prop="mobile">
                <el-input v-model.trim="formModel.mobile" maxlength="11" oninput="value=value.replace(/[^\d]/g,'')"/>
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input show-password v-model.trim="formModel.password" maxlength="30"/>
              </el-form-item>
              <el-form-item label="确认密码" prop="confPassword">
                <el-input show-password v-model.trim="formModel.confPassword" maxlength="30"/>
              </el-form-item>
              <el-form-item class="form-button">
                <el-button type="warning" @click="doSubmit">
                  注册
                </el-button>
              </el-form-item>
            </el-form>
            <div class="login-footer">
              <router-link to="/login" class="el-link">已有账号？点击登录</router-link>
              <router-link to="/forgetPassword" class="el-link">忘记密码？点击重置</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/*导入自定义样式文件*/
import '@/style/css_user.css'
import { projectNameGlobal } from "@/tool/public"
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import request from "@/tool/request"
import { handleValidateConfpassword, handleValidateMobile } from "@/tool/tool"

//获取全局路由器实例对象
const router = useRouter()

//创建表单组件的引用实例对象，可调用表单的属性和方法
const formRef = ref()
//创建表单数据的响应式对象
const formModel = reactive({})

//创建页面的响应式数据对象
const data = reactive({
  formRules: { //表单数据校验规则对象
    loginname: [
      { required: true, message: '请输入用户名', trigger: 'blur' },
      { min: 5, message: '长度最少5位', trigger: 'blur' }
    ],
    mobile: [
      { required: true, message: '请输入电话', trigger: 'blur' },
      { validator: handleValidateMobile, trigger: 'blur' } //电话格式校验
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 5, message: '长度最少5位', trigger: 'blur' }
    ],
    confPassword: [
      { required: true, message: '请输入确认密码', trigger: 'blur' },
      { min: 5, message: '长度最少5位', trigger: 'blur' },
      { validator: handleValidateConfpassword(formModel), trigger: 'blur' } //密码和确认密码是否相同校验
    ]
  }
})

//提交注册数据
const doSubmit = () => {
  //校验表单数据
  formRef.value.validate((valid) => {
    if (valid) {
      //提交数据
      request.post('/user/public/doRegister', formModel).then(res => {
        if (res.success > 0) {//注册成功
          router.push('/login') //跳转到登录页面
        }
      })
    }
  })
}
</script>

<style scoped>

</style>
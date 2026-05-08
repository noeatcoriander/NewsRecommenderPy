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
              <div style="font-size: 1.2rem;margin: 10px 0 0 0;color: #582F0E;font-weight: normal;">忘记密码</div>
            </h5>
          </div>
          <div class="login-form">
            <el-form ref="formRef" :rules="data.formRules" :model="data.formModel" label-width="auto" size="large"
                     label-suffix="：">
              <el-form-item label="用户名" prop="loginname">
                <el-input v-model.trim="data.formModel.loginname" maxlength="30"/>
              </el-form-item>
              <el-form-item label="电话" prop="mobile">
                <el-input v-model.trim="data.formModel.mobile" maxlength="11"
                          oninput="value=value.replace(/[^\d]/g,'')"/>
              </el-form-item>
              <el-form-item class="form-button">
                <el-button type="warning" @click="doSubmit">
                  重置
                </el-button>
              </el-form-item>
            </el-form>
            <div class="login-footer">
              <router-link to="/login" class="el-link">已有账号？点击登录</router-link>
              <router-link to="/register" class="el-link">没有账号？点击注册</router-link>
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
import { reactive, ref } from "vue"
import { useRouter } from 'vue-router'
import request from "@/tool/request"
import { handleValidateMobile } from "@/tool/tool"

//获取全局路由器实例对象
const router = useRouter()

//创建表单组件的引用实例对象，可调用表单的属性和方法
const formRef = ref()

//创建页面的响应式数据对象
const data = reactive({
  formModel: {}, //表单数据对象
  formRules: { //表单数据校验规则对象
    loginname: [
      { required: true, message: '请输入用户名', trigger: 'blur' }
    ],
    mobile: [
      { required: true, message: '请输入电话', trigger: 'blur' },
      { validator: handleValidateMobile, trigger: 'blur' } //电话格式校验
    ]
  }
})

//提交函数
const doSubmit = () => {
  //校验表单数据
  formRef.value.validate((valid) => {
    if (valid) {
      //提交数据
      request.post('/user/public/doForgetPassword', data.formModel).then(res => {
        if (res.success > 0) {//操作成功
          router.push('/login') //跳转到登录页面
        }
      })
    }
  })
}
</script>

<style scoped>

</style>
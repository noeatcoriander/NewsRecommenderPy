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
              <div style="font-size: 1.2rem;margin: 10px 0 0 0;color: #582F0E;font-weight: normal;">用户登录</div>
            </h5>
          </div>
          <div class="login-form">
            <el-form ref="formRef" :rules="data.formRules" :model="data.formModel" label-width="auto" size="large"
                     label-suffix="：">
              <el-form-item label="登录账号" prop="loginname">
                <el-input v-model.trim="data.formModel.loginname" placeholder="用户名、电话、邮箱" maxlength="50"/>
              </el-form-item>
              <el-form-item label="登录密码" prop="password">
                <el-input show-password v-model.trim="data.formModel.password" maxlength="30"/>
              </el-form-item>
              <el-form-item class="form-button">
                <el-button type="warning" @click="doSubmit">
                  登录
                </el-button>
              </el-form-item>
            </el-form>
            <div class="login-footer">
              <router-link to="/register" class="el-link">没有账号？点击注册</router-link>
              <router-link to="/forgetPassword" class="el-link">忘记密码？点击重置</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!--选择兴趣标签对话框-->
  <el-dialog v-model="data.showDialog" title="兴趣标签（可选）" @close="handleCloseDialog" size="large" width="58%">
    <div style="margin: 20px 10%">
      <el-checkbox-group v-model="data.selectNewstypeList">
        <el-checkbox v-for="newstype in data.newstypeList" :key="newstype.id" style="min-width: 80px;"
                     :label="newstype.newstypename" :value="newstype.id" size="large"/>
      </el-checkbox-group>
      <div style="display: flex;justify-content: center;margin-top: 40px">
        <el-button type="info" @click="handleCloseDialog">
          跳过
        </el-button>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <el-button type="warning" @click="doUserlabel">
          提交
        </el-button>
      </div>
    </div>
  </el-dialog>

</template>

<script setup>
/*导入自定义样式文件*/
import '@/style/css_user.css'
import { projectNameGlobal } from "@/tool/public"
import { reactive, ref } from "vue"
import request from "@/tool/request"
import { ElMessage } from "element-plus"
import { useRouter } from 'vue-router'
import { useUserStore } from "@/store/userStore"

//获取全局路由器实例对象
const router = useRouter()

//创建表单组件的引用实例对象，可调用表单的属性和方法
const formRef = ref()

//创建页面的响应式数据对象
const data = reactive({
  userid: '', //当前登录用户id
  showDialog: false, //对话框是否打开
  selectNewstypeList: [], //选中的兴趣标签列表
  newstypeList: [], //标签列表（新闻类型列表）
  formModel: {}, //表单数据对象
  formRules: { //表单数据校验规则对象
    loginname: [
      { required: true, message: '请输入登录账号', trigger: 'blur' }
    ],
    password: [
      { required: true, message: '请输入登录密码', trigger: 'blur' }
    ]
  }
})

//保存选择的兴趣标签函数
const doUserlabel = () => {
  //判断是否选中了标签
  if (data.selectNewstypeList.length === 0) {
    ElMessage.error('请至少选择一个兴趣标签！')
  } else {
    //获取选中的标签列表（新闻类型列表）
    const selectNewstypeidList = Object.values(data.selectNewstypeList)
    //提交数据
    request.post('/user/userlabel/doSave', {
      userid: data.userid, newstypeidList: selectNewstypeidList
    }).then(res => {
      if (res.success > 0) {
        data.showDialog = false //关闭dialog对话框
      }
    })
  }
}

//提交登录数据
const doSubmit = () => {
  //校验表单数据
  formRef.value.validate((valid) => {
    if (valid) {
      //提交数据
      request.post('/user/public/doLogin', data.formModel).then(res => {
        if (res.success > 0) {//登录成功
          //登录成功，获取用户状态管理实例对象和token，并保存token及登录用户信息
          useUserStore().doSave(res.user, res.token)
          //判断用户是否选择了兴趣标签
          if (res.newstypeList && res.newstypeList.length > 0) {
            //用户没有选择兴趣标签
            data.userid = res.user.id //获取登录用户id
            data.newstypeList = res.newstypeList //获取新闻类型列表
            data.showDialog = true //打开dialog对话框
          } else {
            //用户已选择了兴趣标签
            router.replace('/') //跳转到首页
          }
        }
      })
    }
  })
}

//关闭dialog对话框函数
const handleCloseDialog = () => {
  router.replace('/') //跳转到首页
}
</script>

<style scoped>

</style>
<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">兴趣标签</div>
    </div>
    <div class="main-content">
      <el-row :gutter="30">
        <el-col :span="5">
          <Menu/>
        </el-col>
        <el-col :span="19">
          <div class="content-right">
            <div>
              <el-form label-width="15%" style="max-width: 90%" label-suffix="：">
                <el-row :gutter="10">
                  <el-col :span="5">
                    <el-form-item label-width="10%" style="margin-top: 10px;">
                      <el-image :src="baseUploadUrlGlobal+userStore.user?.avatar" fit="fill"
                                style="width: 100%;"/>
                    </el-form-item>
                  </el-col>
                  <el-col :span="19">
                    <el-form-item>
                      <el-checkbox-group v-model="data.selectNewstypeList">
                        <el-checkbox v-for="newstype in data.newstypeList" :key="newstype.id"
                                     :label="newstype.newstypename" :value="newstype.id"
                                     :checked="newstype.flag" size="large" style="min-width: 80px;"/>
                      </el-checkbox-group>
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
import { reactive } from 'vue'
import request from "@/tool/request"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"
import { useUserStore } from "@/store/userStore"
import { baseUploadUrlGlobal } from "@/tool/public"

//获取全局路由器实例对象
const router = useRouter()
//获取当前登录用户的状态管理实例对象
const userStore = useUserStore()

//创建页面的响应式数据对象
const data = reactive({
  newstypeList: [], //新闻类型列表
  selectNewstypeList: [] //选中的新闻类型列表
})

//加载数据函数
const loadData = () => {
  //请求数据
  request.get('/user/userlabel/list').then(res => {
    data.newstypeList = res.newstypeList //新闻类型列表
  })
}

//提交数据
const doSubmit = () => {
  if (data.selectNewstypeList.length === 0) {
    ElMessage.error('请至少选择一个标签！')
  } else {
    //获取新闻类型id
    const selectNewstypeidList = Object.values(data.selectNewstypeList)
    //提交数据
    request.post('/user/userlabel/doUpdate', selectNewstypeidList)
  }
}

//加载数据
loadData()
</script>

<style scoped>

</style>
<template>
  <div class="main-container">
    <div class="main-title">
      <div class="title-name">我的收藏</div>
    </div>
    <div class="main-content">
      <el-row :gutter="30">
        <el-col :span="5">
          <Menu/>
        </el-col>
        <el-col :span="19">
          <div class="content-right">
            <div style="margin-bottom: 10px;text-align: right;">
              <el-button type="warning" @click="doDelete(null, true)">批量删除</el-button>
            </div>
            <div>
              <el-table ref="tableRef" :data="data.userfavorList" size="large"
                        :header-row-style="{'font-weight': 'bold', 'color': '#582F0E', 'font-size': '15px'}">
                <el-table-column type="selection" width="50"/>
                <el-table-column label="新闻" width="420">
                  <template #default="scope">
                    <div style="display: flex;align-items: center;">
                      <img v-if="scope.row.news.photo" :src="baseUploadUrlGlobal+scope.row.news.photo"
                           style="width: 100px;max-height: 100px;margin-right: 10px;">
                      <router-link class="el-link text-break" :to="'/user/news/detail?newsid='+scope.row.news.id">
                        {{ scope.row.news.title }}
                      </router-link>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="收藏时间" prop="savedate" width="200"/>
                <el-table-column label="操作">
                  <template #default="scope">
                    <el-button link type="primary" @click="doDelete(scope.row.id)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>
              <!--分页-->
              <div class="pagination">
                <el-pagination
                    style="overflow: auto"
                    v-model:current-page="data.pageNum"
                    v-model:page-size="data.pageSize"
                    :total="data.total"
                    :page-sizes="pageSizesGlobal"
                    background
                    layout="total, sizes, prev, pager, next, jumper"/>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import Menu from "@/components/user/Menu.vue"
import { reactive, ref, watch } from 'vue'
import { useRouter } from "vue-router"
import { baseUploadUrlGlobal, pageSizeGlobal, pageSizesGlobal } from "@/tool/public"
import request from "@/tool/request"
import { handleDeleteBatch } from "@/tool/tool"

//获取全局路由器实例对象
const router = useRouter()

//创建表格组件的引用实例对象，可调用表格的属性和方法
const tableRef = ref()

//创建页面的响应式数据对象
const data = reactive({
  userfavorList: [], //收藏列表
  pageNum: 1, //分页，当前页数
  pageSize: pageSizeGlobal, //分页，每页条数
  total: 0 //分页，数据总量
})

//加载数据函数
const loadData = () => {
  //请求数据
  request.get('/user/userfavor/list', {
    params: { pageNum: data.pageNum, pageSize: data.pageSize }
  }).then(res => {
    data.userfavorList = res.pageBean.list //收藏列表
    data.total = res.pageBean.total //分页，数据总量
  })
}

//删除函数
const doDelete = (selectIds, isBatch = false) => {
  if (selectIds === undefined) {//删除数据未定义
    return
  }
  if (isBatch) {//批量删除
    //getSelectionRows()：el-table表格暴露的内置方法，获取选中的行数据
    let selectedRows = tableRef.value.getSelectionRows()
    selectIds = selectedRows.map(row => row.id) //获取选中的id，数组格式
  } else {//单个删除
    selectIds = [selectIds] //转数组格式
  }
  //调用公共删除函数
  handleDeleteBatch(selectIds, '/user/userfavor/doDelete', loadData)
}

//vue watch监听事件，监听分页页码和每页显示数量的改变，改变后重新加载数据
watch(
    () => [data.pageNum, data.pageSize],
    () => {
      loadData() //加载数据
    }
)

//加载数据
loadData()
</script>

<style scoped>

</style>
<template>
  <div class="dynamic-table-container page-container">
    <div class="page-header">
      <h1 class="page-title">{{ tableDefinition?.display_name || '数据表' }}</h1>
      <el-button type="primary" @click="showCreateForm">添加数据</el-button>
    </div>
    
    <div class="page-content">
      <!-- Table display -->
      <el-card v-if="!loading">
        <template #header>
          <div class="card-header">
            <div class="search-container">
              <el-input 
                v-model="searchQuery" 
                placeholder="搜索..." 
                clearable
                :prefix-icon="Search" />
            </div>
            
            <div class="table-actions">
              <el-button type="primary" plain @click="refreshData">刷新</el-button>
            </div>
          </div>
        </template>
        
        <el-table 
          :data="filteredTableData" 
          border 
          style="width: 100%"
          v-loading="loading">
          <!-- Dynamic columns based on table fields -->
          <el-table-column 
            v-for="field in fields" 
            :key="field.name"
            :prop="field.name"
            :label="field.display_name"
            :min-width="getColumnWidth(field.field_type)">
            <template #default="scope">
              <span>{{ formatCellValue(scope.row[field.name], field.field_type) }}</span>
            </template>
          </el-table-column>
          
          <!-- Action column -->
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button 
                type="text" 
                size="small" 
                @click="editRecord(scope.row)">
                编辑
              </el-button>
              <el-button 
                type="text" 
                size="small" 
                class="delete-btn"
                @click="confirmDeleteRecord(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- Pagination -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.per_page"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange" />
        </div>
      </el-card>
      
      <el-skeleton v-else :rows="6" animated />
    </div>
    
    <!-- Form dialog for create/edit -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="isEditing ? '编辑数据' : '添加数据'" 
      width="600px">
      <el-form 
        ref="recordFormRef" 
        :model="recordForm" 
        :rules="formRules" 
        label-width="100px">
        <el-form-item 
          v-for="field in fields" 
          :key="field.name"
          :label="field.display_name"
          :prop="field.name"
          :rules="getFieldRules(field)">
          
          <!-- Text input -->
          <el-input 
            v-if="field.field_type === 'text'" 
            v-model="recordForm[field.name]"
            :placeholder="`请输入${field.display_name}`" />
          
          <!-- Long text (textarea) -->
          <el-input 
            v-else-if="field.field_type === 'longtext'" 
            v-model="recordForm[field.name]"
            :placeholder="`请输入${field.display_name}`"
            type="textarea"
            :rows="4" />
          
          <!-- Number input -->
          <el-input-number 
            v-else-if="field.field_type === 'number'" 
            v-model="recordForm[field.name]"
            :precision="2"
            :step="0.1"
            style="width: 100%;" />
          
          <!-- Integer input -->
          <el-input-number 
            v-else-if="field.field_type === 'integer'" 
            v-model="recordForm[field.name]"
            :precision="0"
            :step="1"
            style="width: 100%;" />
          
          <!-- Date picker -->
          <el-date-picker 
            v-else-if="field.field_type === 'date'" 
            v-model="recordForm[field.name]"
            type="date"
            :placeholder="`选择${field.display_name}`"
            style="width: 100%;" />
          
          <!-- Datetime picker -->
          <el-date-picker 
            v-else-if="field.field_type === 'datetime'" 
            v-model="recordForm[field.name]"
            type="datetime"
            :placeholder="`选择${field.display_name}`"
            style="width: 100%;" />
          
          <!-- Boolean (switch) -->
          <el-switch 
            v-else-if="field.field_type === 'boolean'" 
            v-model="recordForm[field.name]" />
          
          <!-- Default text input for any other type -->
          <el-input 
            v-else 
            v-model="recordForm[field.name]"
            :placeholder="`请输入${field.display_name}`" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">
            {{ isEditing ? '保存' : '添加' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

// Props
const props = defineProps({
  tableName: {
    type: String,
    required: true
  }
})

// Route and data
const route = useRoute()
const tableName = computed(() => props.tableName)
const tableDefinition = ref(null)
const fields = ref([])
const tableData = ref([])
const loading = ref(true)
const dialogVisible = ref(false)
const isEditing = ref(false)
const currentRecord = ref(null)
const recordFormRef = ref(null)
const recordForm = reactive({})
const submitLoading = ref(false)
const searchQuery = ref('')

// Pagination
const pagination = reactive({
  page: 1,
  per_page: 10,
  total: 0
})

// Computed properties
const filteredTableData = computed(() => {
  if (!searchQuery.value) return tableData.value
  
  const query = searchQuery.value.toLowerCase()
  return tableData.value.filter(row => {
    return fields.value.some(field => {
      const value = row[field.name]
      if (value === null || value === undefined) return false
      return String(value).toLowerCase().includes(query)
    })
  })
})

// Form rules
const formRules = computed(() => {
  const rules = {}
  
  fields.value.forEach(field => {
    if (field.required) {
      rules[field.name] = [
        { required: true, message: `${field.display_name}不能为空`, trigger: 'blur' }
      ]
    }
  })
  
  return rules
})

// Watch for table name changes
watch(() => props.tableName, () => {
  loadTableDefinition()
}, { immediate: true })

// Lifecycle hooks
onMounted(() => {
  loadTableDefinition()
})

// Methods
async function loadTableDefinition() {
  loading.value = true
  try {
    // Get all tables
    const response = await axios.get('/api/tables/')
    const tables = response.data.tables
    
    // Find the current table by name
    tableDefinition.value = tables.find(table => table.name === tableName.value)
    
    if (tableDefinition.value) {
      fields.value = tableDefinition.value.fields
      await fetchTableData()
    } else {
      ElMessage.error('表格不存在')
    }
  } catch (error) {
    console.error('Failed to load table definition:', error)
    ElMessage.error('加载表格失败')
  } finally {
    loading.value = false
  }
}

async function fetchTableData() {
  loading.value = true
  try {
    const response = await axios.get(`/api/dynamic/${tableName.value}`, {
      params: {
        page: pagination.page,
        per_page: pagination.per_page
      }
    })
    tableData.value = response.data.data
    pagination.total = response.data.pagination.total
  } catch (error) {
    console.error('Failed to fetch table data:', error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

function getColumnWidth(fieldType) {
  switch (fieldType) {
    case 'text': return 180
    case 'longtext': return 300
    case 'number': return 120
    case 'integer': return 100
    case 'date': return 120
    case 'datetime': return 180
    case 'boolean': return 80
    default: return 150
  }
}

function formatCellValue(value, fieldType) {
  if (value === null || value === undefined) return ''
  
  switch (fieldType) {
    case 'date':
      return new Date(value).toLocaleDateString()
    case 'datetime':
      return new Date(value).toLocaleString()
    case 'boolean':
      return value ? '是' : '否'
    default:
      return value
  }
}

function getFieldRules(field) {
  const rules = []
  
  if (field.required) {
    rules.push({ required: true, message: `${field.display_name}不能为空`, trigger: 'blur' })
  }
  
  // Add additional validation based on field type
  switch (field.field_type) {
    case 'number':
      rules.push({ type: 'number', message: '请输入有效的数字', trigger: 'blur' })
      break
    case 'integer':
      rules.push({ type: 'number', message: '请输入有效的整数', trigger: 'blur' })
      break
    case 'date':
    case 'datetime':
      rules.push({ type: 'date', message: '请选择有效的日期', trigger: 'change' })
      break
  }
  
  return rules
}

function showCreateForm() {
  isEditing.value = false
  currentRecord.value = null
  
  // Reset form
  Object.keys(recordForm).forEach(key => delete recordForm[key])
  
  // Set default values
  fields.value.forEach(field => {
    if (field.default_value) {
      recordForm[field.name] = field.default_value
    } else {
      // Initialize with empty values based on type
      switch (field.field_type) {
        case 'number':
        case 'integer':
          recordForm[field.name] = null
          break
        case 'boolean':
          recordForm[field.name] = false
          break
        default:
          recordForm[field.name] = ''
      }
    }
  })
  
  dialogVisible.value = true
}

function editRecord(record) {
  isEditing.value = true
  currentRecord.value = record
  
  // Reset form
  Object.keys(recordForm).forEach(key => delete recordForm[key])
  
  // Populate form with record data
  fields.value.forEach(field => {
    let value = record[field.name]
    
    // Handle date types
    if ((field.field_type === 'date' || field.field_type === 'datetime') && value) {
      value = new Date(value)
    }
    
    recordForm[field.name] = value
  })
  
  dialogVisible.value = true
}

async function submitForm() {
  if (!recordFormRef.value) return
  
  try {
    await recordFormRef.value.validate()
    
    submitLoading.value = true
    
    // Clone the form data to avoid reactivity issues
    const formData = { ...recordForm }
    
    // 过滤掉所有null和undefined值，避免后端处理问题
    Object.keys(formData).forEach(key => {
      if (formData[key] === null || formData[key] === undefined) {
        // 根据字段类型设置适当的默认值
        const field = fields.value.find(f => f.name === key)
        if (field) {
          switch (field.field_type) {
            case 'number':
            case 'integer':
              formData[key] = 0;
              break;
            case 'boolean':
              formData[key] = false;
              break;
            default:
              formData[key] = '';
          }
        } else {
          delete formData[key]; // 如果找不到对应字段，则删除该属性
        }
      }
    });
    
    // Format dates for API
    fields.value.forEach(field => {
      if ((field.field_type === 'date' || field.field_type === 'datetime') && formData[field.name]) {
        try {
          formData[field.name] = new Date(formData[field.name]).toISOString()
        } catch (e) {
          console.error(`转换日期字段失败 [${field.name}]:`, e)
          formData[field.name] = null
        }
      }
    })
    
    console.log('准备提交数据:', formData);
    
    if (isEditing.value) {
      // Update existing record
      const response = await axios.put(`/api/dynamic/${tableName.value}/${currentRecord.value.id}`, formData)
      console.log('更新响应:', response.data);
      ElMessage.success('更新成功')
    } else {
      // Create new record
      const response = await axios.post(`/api/dynamic/${tableName.value}`, formData)
      console.log('创建响应:', response.data);
      ElMessage.success('添加成功')
    }
    
    // Refresh data and close dialog
    await fetchTableData()
    dialogVisible.value = false
  } catch (error) {
    console.error('提交表单失败:', error);
    if (error.response) {
      console.error('错误状态码:', error.response.status);
      console.error('错误详情:', error.response.data);
      
      if (error.response.data?.message) {
        ElMessage.error(error.response.data.message)
      } else {
        ElMessage.error(isEditing.value ? '更新失败: 服务器错误' : '添加失败: 服务器错误')
      }
    } else if (error.request) {
      ElMessage.error('网络错误，无法连接到服务器')
    } else {
      ElMessage.error(isEditing.value ? '更新失败' : '添加失败')
    }
  } finally {
    submitLoading.value = false
  }
}

async function confirmDeleteRecord(record) {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条记录吗？此操作无法恢复。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    loading.value = true
    
    // Delete record
    await axios.delete(`/api/dynamic/${tableName.value}/${record.id}`)
    
    ElMessage.success('删除成功')
    
    // Refresh data
    await fetchTableData()
  } catch (error) {
    if (error === 'cancel') return
    
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else {
      ElMessage.error('删除失败')
    }
  } finally {
    loading.value = false
  }
}

function refreshData() {
  fetchTableData()
}

function handleSizeChange(size) {
  pagination.per_page = size
  fetchTableData()
}

function handleCurrentChange(page) {
  pagination.page = page
  fetchTableData()
}
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .search-container {
    width: 300px;
  }
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.delete-btn {
  color: var(--danger-color);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style> 
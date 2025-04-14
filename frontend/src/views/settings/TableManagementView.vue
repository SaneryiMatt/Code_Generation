<template>
  <div class="table-management-container page-container">
    <div class="page-header">
      <h1 class="page-title">表格管理</h1>
      <el-button type="primary" @click="showCreateTable">创建新表格</el-button>
    </div>
    
    <div class="page-content">
      <!-- Table list -->
      <el-card v-if="tables.length">
        <template #header>
          <div class="card-header">
            <h3>现有表格</h3>
          </div>
        </template>
        
        <el-table :data="tables" style="width: 100%">
          <el-table-column prop="name" label="表格名称" width="180" />
          <el-table-column prop="display_name" label="显示名称" width="180" />
          <el-table-column prop="description" label="描述" />
          <el-table-column prop="fields.length" label="字段数量" width="100" />
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button 
                type="text" 
                size="small" 
                @click="viewTableDetails(scope.row)">
                查看
              </el-button>
              <el-button 
                type="text" 
                size="small" 
                class="delete-btn"
                @click="confirmDeleteTable(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      
      <el-empty v-else description="暂无表格，请点击创建按钮添加" />
    </div>
    
    <!-- Create table dialog -->
    <el-dialog 
      v-model="dialogVisible" 
      title="创建新表格" 
      width="800px"
      :close-on-click-modal="false">
      <el-form 
        ref="tableFormRef" 
        :model="tableForm" 
        :rules="rules" 
        label-width="120px"
        class="table-form">
        <el-form-item label="表格名称" prop="name">
          <el-input 
            v-model="tableForm.name" 
            placeholder="请输入表格名称（英文字母、数字和下划线）">
            <template #prepend>dynamic_</template>
          </el-input>
          <div class="form-help">用于数据库中的表名，仅支持英文字母、数字和下划线</div>
        </el-form-item>
        
        <el-form-item label="显示名称" prop="display_name">
          <el-input v-model="tableForm.display_name" placeholder="请输入显示名称" />
          <div class="form-help">显示在界面上的名称</div>
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="tableForm.description" 
            type="textarea" 
            placeholder="请输入表格描述" />
        </el-form-item>
        
        <el-divider content-position="center">表格字段</el-divider>
        
        <div v-for="(field, index) in tableForm.fields" :key="index" class="field-item">
          <div class="field-header">
            <h4>字段 #{{ index + 1 }}</h4>
            <el-button 
              type="danger" 
              circle 
              plain
              :icon="Delete"
              @click="removeField(index)"
              :disabled="tableForm.fields.length <= 1" />
          </div>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item 
                :prop="`fields.${index}.name`"
                :rules="[
                  { required: true, message: '字段名称不能为空', trigger: 'blur' },
                  { pattern: /^[a-zA-Z][a-zA-Z0-9_]*$/, message: '字段名称仅支持字母开头，包含字母、数字和下划线', trigger: 'blur' }
                ]">
                <template #label>
                  <span class="required-field">字段名称</span>
                </template>
                <el-input v-model="field.name" placeholder="字段名称（英文）" />
              </el-form-item>
            </el-col>
            
            <el-col :span="12">
              <el-form-item 
                :prop="`fields.${index}.display_name`"
                :rules="[
                  { required: true, message: '显示名称不能为空', trigger: 'blur' }
                ]">
                <template #label>
                  <span class="required-field">显示名称</span>
                </template>
                <el-input v-model="field.display_name" placeholder="显示名称" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item 
                :prop="`fields.${index}.field_type`"
                :rules="[
                  { required: true, message: '字段类型不能为空', trigger: 'change' }
                ]">
                <template #label>
                  <span class="required-field">字段类型</span>
                </template>
                <el-select v-model="field.field_type" placeholder="请选择" style="width: 100%">
                  <el-option label="文本" value="text" />
                  <el-option label="长文本" value="longtext" />
                  <el-option label="数字" value="number" />
                  <el-option label="整数" value="integer" />
                  <el-option label="日期" value="date" />
                  <el-option label="日期时间" value="datetime" />
                  <el-option label="布尔值" value="boolean" />
                </el-select>
              </el-form-item>
            </el-col>
            
            <el-col :span="12">
              <el-form-item>
                <template #label>
                  <span>必填</span>
                </template>
                <el-switch v-model="field.required" />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-form-item label="默认值" :prop="`fields.${index}.default_value`">
            <el-input v-model="field.default_value" placeholder="默认值" />
          </el-form-item>
        </div>
        
        <el-form-item>
          <el-button type="primary" plain @click="addField">添加字段</el-button>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="loading">
            创建表格
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- View table details dialog -->
    <el-dialog v-model="detailsVisible" title="表格详情" width="700px">
      <template v-if="selectedTable">
        <div class="details-item">
          <h4>基本信息</h4>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="表格名称">{{ selectedTable.name }}</el-descriptions-item>
            <el-descriptions-item label="显示名称">{{ selectedTable.display_name }}</el-descriptions-item>
            <el-descriptions-item label="描述">{{ selectedTable.description || '无' }}</el-descriptions-item>
          </el-descriptions>
        </div>
        
        <div class="details-item">
          <h4>字段信息</h4>
          <el-table :data="selectedTable.fields" border>
            <el-table-column prop="name" label="字段名称" width="120" />
            <el-table-column prop="display_name" label="显示名称" width="120" />
            <el-table-column prop="field_type" label="类型" width="100">
              <template #default="scope">
                {{ getFieldTypeLabel(scope.row.field_type) }}
              </template>
            </el-table-column>
            <el-table-column prop="required" label="必填" width="80">
              <template #default="scope">
                <el-tag :type="scope.row.required ? 'danger' : 'info'">
                  {{ scope.row.required ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="default_value" label="默认值">
              <template #default="scope">
                {{ scope.row.default_value || '无' }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { Delete } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useMenuStore } from '@/stores/menu'
import { addDynamicTableRoutes } from '@/router'

const menuStore = useMenuStore()
const dialogVisible = ref(false)
const detailsVisible = ref(false)
const loading = ref(false)
const tables = ref([])
const selectedTable = ref(null)
const tableFormRef = ref(null)

// Form data
const tableForm = reactive({
  name: '',
  display_name: '',
  description: '',
  fields: [
    {
      name: '',
      display_name: '',
      field_type: '',
      required: false,
      default_value: ''
    }
  ]
})

// Form validation rules
const rules = {
  name: [
    { required: true, message: '表格名称不能为空', trigger: 'blur' },
    { pattern: /^[a-zA-Z][a-zA-Z0-9_]*$/, message: '表格名称仅支持字母开头，包含字母、数字和下划线', trigger: 'blur' }
  ],
  display_name: [
    { required: true, message: '显示名称不能为空', trigger: 'blur' }
  ],
  fields: [
    { 
      type: 'array', 
      required: true,
      message: '至少需要一个字段', 
      trigger: 'change'
    }
  ]
}

// Load tables on component mount
onMounted(async () => {
  await fetchTables()
})

// Methods
async function fetchTables() {
  try {
    const response = await axios.get('/api/tables/')
    tables.value = response.data.tables
  } catch (error) {
    console.error('Failed to fetch tables:', error)
    ElMessage.error('获取表格列表失败')
  }
}

function showCreateTable() {
  resetForm()
  dialogVisible.value = true
}

function resetForm() {
  // 重置主表单
  tableForm.name = ''
  tableForm.display_name = ''
  tableForm.description = ''
  
  // 重置字段为只有一个默认字段
  tableForm.fields = [{
    name: '',
    display_name: '',
    field_type: 'text',
    required: false,
    default_value: ''
  }]
  
  // 如果表单引用存在，调用重置方法
  if (tableFormRef.value) {
    tableFormRef.value.resetFields()
  }
}

function addField() {
  tableForm.fields.push({
    name: '',
    display_name: '',
    field_type: '',
    required: false,
    default_value: ''
  })
}

function removeField(index) {
  if (tableForm.fields.length > 1) {
    tableForm.fields.splice(index, 1)
  }
}

async function submitForm() {
  try {
    // 验证表单
    await tableFormRef.value.validate()
    
    // 验证字段名称不重复
    const fieldNames = tableForm.fields.map(field => field.name);
    const duplicateFieldNames = fieldNames.filter((name, index) => 
      fieldNames.indexOf(name) !== index
    );
    
    if (duplicateFieldNames.length > 0) {
      ElMessage.error(`存在重复的字段名称: ${duplicateFieldNames.join(', ')}`);
      return;
    }
    
    // 验证字段显示名称不重复
    const fieldDisplayNames = tableForm.fields.map(field => field.display_name);
    const duplicateDisplayNames = fieldDisplayNames.filter((name, index) => 
      fieldDisplayNames.indexOf(name) !== index
    );
    
    if (duplicateDisplayNames.length > 0) {
      ElMessage.error(`存在重复的字段显示名称: ${duplicateDisplayNames.join(', ')}`);
      return;
    }
    
    loading.value = true
    
    // 提交表单到API
    const response = await axios.post('/api/tables/', tableForm)
    
    if (response.data && response.status === 201) {
      // Add to menu
      const newTable = response.data.table;
      // 确保路径格式正确，统一使用绝对路径
      const tablePath = `/tables/${newTable.name}`;

      console.log('表格创建成功，准备添加菜单项:', {
        name: `table-${newTable.name}`,
        display_name: newTable.display_name,
        path: tablePath
      });

      // 重要：先把新建表格添加到菜单
      menuStore.addTableMenuItem({
        name: `table-${newTable.name}`,
        display_name: newTable.display_name,
        path: tablePath,
        icon: 'grid'
      });

      // 重置表单和关闭对话框
      resetForm();
      dialogVisible.value = false;

      // 使用Promise.all等待所有刷新操作完成
      Promise.all([
        // 刷新表格列表
        fetchTables(),
        // 强制刷新菜单，确保菜单项正确显示
        menuStore.fetchMenu()
      ]).then(() => {
        // 所有刷新操作完成后，再次确保动态路由已添加
        setTimeout(() => {
          // 再次触发动态路由添加
          addDynamicTableRoutes();
          
          ElMessage({
            message: '表格创建完成，可以在左侧菜单访问',
            type: 'success',
            duration: 5000
          });
        }, 500);
      });
    }
  } catch (error) {
    console.error('表格创建错误:', error);
    // 防止重复显示错误消息
    if (error.response?.data?.message) {
      ElMessage.error(`表格创建失败: ${error.response.data.message}`)
    } else {
      ElMessage.error('表格创建失败，请检查网络连接或联系管理员')
    }
  } finally {
    loading.value = false
  }
}

function viewTableDetails(table) {
  selectedTable.value = table
  detailsVisible.value = true
}

function getFieldTypeLabel(type) {
  const typeMap = {
    'text': '文本',
    'longtext': '长文本',
    'number': '数字',
    'integer': '整数',
    'date': '日期',
    'datetime': '日期时间',
    'boolean': '布尔值'
  }
  return typeMap[type] || type
}

async function confirmDeleteTable(table) {
  try {
    await ElMessageBox.confirm(
      `确定要删除表格 "${table.display_name}" 吗？这将删除该表格的所有数据，且无法恢复。`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    loading.value = true
    
    // Delete table from API
    await axios.delete(`/api/tables/${table.id}`)
    
    ElMessage.success('表格删除成功')
    
    // Refresh table list and menu
    await fetchTables()
    await menuStore.fetchMenu()
    
  } catch (error) {
    if (error === 'cancel') return
    
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.message)
    } else {
      ElMessage.error('表格删除失败')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.delete-btn {
  color: var(--danger-color);
}

.field-item {
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  margin-bottom: 16px;
  
  .field-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    h4 {
      margin: 0;
    }
  }
}

.required-field::before {
  content: '*';
  color: var(--danger-color);
  margin-right: 4px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.form-help {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.details-item {
  margin-bottom: 24px;
  
  h4 {
    margin-bottom: 12px;
  }
}
</style> 
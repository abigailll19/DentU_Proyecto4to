import { createRouter, createWebHistory } from 'vue-router'

// IMPORTA AQUÍ TUS VISTAS/COMPONENTES
import registroView           from '../views/RegistroView.vue'
import panel_odontologoView   from '../views/Panel_odontologoView.vue'
import panel_adminView            from '../views/Panel_adminView.vue'
import odontogramaView from '../views/odontogramaView.vue'
import busqueda_pacientes_adminView   from '../views/busqueda_pacientes_adminView.vue'
import agregar_paciente_adminView   from '../views/agregar_paciente_adminView.vue'

// … importa las demás vistas que tengas

const routes = [
  { path: '/',                name: 'registro',                component: registroView },
  { path: '/panel_odontologo',        name: 'panel_odontologo',        component: panel_odontologoView },
  { path: '/panel_admin',             name: 'panel_admin',             component: panel_adminView },
  { path: '/odontograma',             name: 'odontograma',             component: odontogramaView },
  { path: '/busqueda_pacientes_admin', name: 'busqueda_pacientes_admin',       component: busqueda_pacientes_adminView },
  { path: '/agregar_paciente_admin',  name: 'agregar_paciente_admin',  component: agregar_paciente_adminView },
]

const router = createRouter({
  history: createWebHistory(), // usa el History API del navegador
  routes
})

export default router

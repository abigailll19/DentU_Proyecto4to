<template>
  <div class="container">
    <div class="header">
      <h1>Sistema Web - Panel Administrador</h1>
      <p>Bienvenido Admin | Hoy, <span id="current-date">{{ currentDate }}</span></p>
    </div>

    <div class="main-content">
      <div class="buttons-grid">
        <button
          class="admin-button btn-red"
          @click="showSection('usuarios')"
        >
          <div class="btn-icon">📅</div>
          <div class="btn-text">
            <div class="btn-title">Agendar citas</div>
            <div class="btn-subtitle">Citas para nuevo paciente</div>
          </div>
        </button>

        <button
          class="admin-button btn-gray"
          @click="showSection('buscar_paciente')"
        >
          <div class="btn-icon">🔍</div>
          <div class="btn-text">
            <div class="btn-title">Buscar paciente</div>
            <div class="btn-subtitle">Consultas e historial</div>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'PanelAdmin',
  data() {
    return {
      currentDate: '' // Definir la propiedad currentDate
    }
  },
  methods: {
    // Método para mostrar secciones - la forma correcta en Vue
    showSection(section) {
      if (section === 'usuarios') {
        this.$router.push('/agregar_paciente_admin')
      } else if (section === 'buscar_paciente') {
        this.$router.push('/busqueda_pacientes_admin')
      }
    }
  },
  mounted() {
    // Obtiene la fecha de hoy y la asigna a la propiedad del componente
    const today = new Date();
    const options = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };
    
    // Asignar a la propiedad del componente en lugar de manipular el DOM directamente
    this.currentDate = today.toLocaleDateString('es-ES', options);
    
    // Si necesitas también actualizar un elemento del DOM (método alternativo)
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
      dateElement.textContent = this.currentDate;
    }

    // Solo si necesitas mantener onclick (arrow function para preservar contexto)
    window.showSection = (section) => {
      this.showSection(section);
    };
  }
}
</script>

<style scoped src="../styles/panel_admin.css"></style>




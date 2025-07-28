<template>
  <div class="login-page">
    <div class="clinic-brand">
      <img
        src="https://www.uleam.edu.ec/wp-content/uploads/2012/09/LOGO-ULEAM-VERTICAL.png"
        alt="Logo Clínica"
        class="logo-imagen"
      />
      ClinicaDent U
    </div>

    <div class="container">
      <div class="header">
        <div class="logo">ClinicaDent U</div>
      </div>

      <div class="form-container">
        <div id="login-form" class="form-section active">
          <form @submit.prevent="submitLogin">
            <div class="form-group">
              <label for="login-email">Correo Electrónico</label>
              <input
                type="email"
                id="login-email"
                v-model.trim="email"
                class="form-control"
                placeholder="Ingresa tu correo electrónico"
                required
              />
            </div>

            <div class="form-group">
              <label for="login-password">Contraseña</label>
              <div class="input-container">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  id="login-password"
                  v-model.trim="password"
                  class="form-control"
                  placeholder="Ingresa tu contraseña"
                  required
                />
                <span class="password-toggle" @click="togglePassword">
                  {{ showPassword ? '🙈' : '👁️' }}
                </span>
              </div>
            </div>

            <button type="submit" class="btn">Iniciar Sesión</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      showPassword: false
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    validarCorreo(gmail) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(gmail)
    },
    submitLogin() {
      if (!this.email || !this.password) {
        return alert('Por favor completa todos los campos de inicio de sesión.')
      }
      if (!this.validarCorreo(this.email)) {
        return alert('Por favor ingresa un correo válido.')
      }

      const usuario = this.email.split('@')[0].toLowerCase()
      localStorage.setItem('usuarioActual', usuario)

      if (this.email.endsWith('@admin.uleam.com')) {
        localStorage.setItem('rol', 'administrador')
        this.$router.push('/panel_admin')
      }
      else if (this.email.endsWith('@odont.uleam.com')) {
        if (usuario === 'garcia' || usuario === 'mendoza') {
          localStorage.setItem('rol', 'odontologo')
          this.$router.push('/panel_odontologo')
        } else {
          alert('Solo se permite el acceso personal autorizado.')
        }
      }
      else {
        alert('Dominio de correo no reconocido. Contacta al administrador.')
      }
    }
  },
  mounted() {
    // Registrar service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
        .register('/sw.js', { scope: '/' })
        .catch(err => console.error('SW registration failed:', err))
    }
  }
}
</script>

<style scoped src="../styles/registro.css"></style>

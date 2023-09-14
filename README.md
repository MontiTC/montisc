# montisc
# Montijo Perez Jose Alejandro 20212676
# Presentación del HC-SR04 UltraSonic Distance Sensor

## Introducción

El HC-SR04 es un sensor ultrasónico de distancia ampliamente utilizado en proyectos electrónicos y robóticos para medir distancias con precisión. Esta presentación te introducirá a sus características y aplicaciones.

---

## Principio de Funcionamiento

- **Emisión de Ondas Ultrasónicas:** El HC-SR04 emite pulsos ultrasónicos hacia un objeto.
- **Recepción del Eco:** El sensor detecta el eco de las ondas reflejadas por el objeto.
- **Cálculo de Distancia:** Utiliza la velocidad del sonido para calcular la distancia al objeto.

---

## Especificaciones Técnicas

- **Rango de Medición:** 2 cm a 400 cm (aproximadamente).
- **Voltaje de Funcionamiento:** 5V.
- **Ángulo de Apertura:** 15 grados.
- **Precisión:** Milímetros.
- **Interfaz:** Pines VCC, Trig, Echo y GND.

---

## Conexiones y Configuración

1. Conecta VCC a 5V, GND a tierra y Trig y Echo a pines GPIO en tu microcontrolador.
2. Envía un pulso corto al pin Trig para activar la emisión ultrasónica.
3. Mide el tiempo que tarda en recibir el eco en el pin Echo.
4. Calcula la distancia utilizando la fórmula: Distancia = Velocidad x Tiempo.

---

## Aplicaciones Comunes

- **Detección de Obstáculos:** En robots y vehículos autónomos.
- **Alarmas de Proximidad:** Para alertar sobre la cercanía de objetos.
- **Domótica:** Para medir distancias entre objetos en proyectos de automatización.
- **Control de Nivel de Líquidos:** En tanques y recipientes.
- **Seguridad:** Detectar intrusos o personas cercanas.

---

## Consideraciones de Uso

- **Variaciones de Velocidad del Sonido:** La velocidad del sonido puede cambiar con la temperatura y la humedad.
- **Evitar Reflejos Múltiples:** Para mediciones precisas, evita superficies reflectantes o ángulos complicados.
- **Superficies Absorbentes:** No funciona bien en superficies que absorben el sonido, como espuma o tela.

---

## Librerías y Ejemplos de Código

- Para proyectos con Arduino o Raspberry Pi, existen librerías y ejemplos de código en línea que facilitan su integración.

---

## Conclusión

El HC-SR04 UltraSonic Distance Sensor es una herramienta versátil y asequible para medir distancias con precisión en proyectos electrónicos y robóticos. Su principio de funcionamiento basado en ultrasonidos lo hace adecuado para una amplia gama de aplicaciones.

¡Gracias por tu atención!


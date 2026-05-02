"""
Librería de clases para el Ejercicio 4 del proyecto.
Debe ubicarse en la misma carpeta que app.py.
"""

from __future__ import annotations


class Empleado:
    def __init__(self, nombre: str, salario_base: float, años_antiguedad: int = 0) -> None:
        self.nombre = nombre
        self.salario_base = float(salario_base)
        self.años_antiguedad = int(años_antiguedad)

    def resumen(self) -> dict:
        bonus = self.salario_base * 0.02 * max(self.años_antiguedad, 0)
        return {
            "nombre": self.nombre,
            "salario_base": round(self.salario_base, 2),
            "años_antiguedad": self.años_antiguedad,
            "salario_con_bonus_estimado": round(self.salario_base + bonus, 2),
        }


class ProyectoInversion:
    def __init__(self, nombre_proyecto: str, tasa_descuento: float, flujos: list[float]) -> None:
        self.nombre_proyecto = nombre_proyecto
        self.tasa_descuento = float(tasa_descuento)
        self.flujos = [float(x) for x in flujos]

    def _vpn_simple(self) -> float:
        """Valor presente neto (periodos discretos), tasa en decimal por periodo."""
        r = self.tasa_descuento / 100.0 if self.tasa_descuento > 1 else self.tasa_descuento
        if r <= -1:
            r = 0.0
        total = 0.0
        for t, f in enumerate(self.flujos, start=1):
            total += f / ((1 + r) ** t)
        return total

    def resumen(self) -> dict:
        return {
            "nombre_proyecto": self.nombre_proyecto,
            "tasa_descuento_pct": round(self.tasa_descuento, 4),
            "num_flujos": len(self.flujos),
            "suma_flujos": round(sum(self.flujos), 2),
            "vpn_estimado": round(self._vpn_simple(), 2),
        }


class InventarioProducto:
    def __init__(self, codigo: str, nombre: str, cantidad: float, precio_unitario: float) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.cantidad = float(cantidad)
        self.precio_unitario = float(precio_unitario)

    def resumen(self) -> dict:
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "cantidad": round(self.cantidad, 3),
            "precio_unitario": round(self.precio_unitario, 4),
            "valor_inventario": round(self.cantidad * self.precio_unitario, 2),
        }


class Servidor:
    def __init__(self, hostname: str, cpus: int, ram_gb: float) -> None:
        self.hostname = hostname
        self.cpus = int(cpus)
        self.ram_gb = float(ram_gb)

    def resumen(self) -> dict:
        return {
            "hostname": self.hostname,
            "cpus": self.cpus,
            "ram_gb": round(self.ram_gb, 2),
            "capacidad_relativa": round(self.cpus * self.ram_gb, 2),
        }


class EquipoMantenimiento:
    def __init__(self, nombre_equipo: str, horas_uso: float, costo_hora: float) -> None:
        self.nombre_equipo = nombre_equipo
        self.horas_uso = float(horas_uso)
        self.costo_hora = float(costo_hora)

    def resumen(self) -> dict:
        return {
            "nombre_equipo": self.nombre_equipo,
            "horas_uso": round(self.horas_uso, 2),
            "costo_hora": round(self.costo_hora, 4),
            "costo_mantenimiento_estimado": round(self.horas_uso * self.costo_hora, 2),
        }


class EstudianteCurso:
    def __init__(self, nombre: str, codigo_estudiante: str, nota: float) -> None:
        self.nombre = nombre
        self.codigo_estudiante = codigo_estudiante
        self.nota = float(nota)

    def resumen(self) -> dict:
        estado = "Aprobado" if self.nota >= 3.0 else "No aprobado"
        return {
            "nombre": self.nombre,
            "codigo_estudiante": self.codigo_estudiante,
            "nota": round(self.nota, 2),
            "estado": estado,
        }


class Paciente:
    def __init__(self, nombre: str, edad: int, peso_kg: float) -> None:
        self.nombre = nombre
        self.edad = int(edad)
        self.peso_kg = float(peso_kg)

    def resumen(self) -> dict:
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "peso_kg": round(self.peso_kg, 2),
            "clasificacion_edad": "Menor" if self.edad < 18 else "Adulto",
        }


class MezclaConcreto:
    def __init__(self, resistencia_mpa: float, volumen_m3: float) -> None:
        self.resistencia_mpa = float(resistencia_mpa)
        self.volumen_m3 = float(volumen_m3)

    def resumen(self) -> dict:
        return {
            "resistencia_mpa": round(self.resistencia_mpa, 2),
            "volumen_m3": round(self.volumen_m3, 3),
            "indice_carga": round(self.resistencia_mpa * self.volumen_m3, 2),
        }


class EspacioIluminacion:
    def __init__(self, largo_m: float, ancho_m: float, lux_objetivo: float) -> None:
        self.largo_m = float(largo_m)
        self.ancho_m = float(ancho_m)
        self.lux_objetivo = float(lux_objetivo)

    def resumen(self) -> dict:
        area = self.largo_m * self.ancho_m
        return {
            "largo_m": round(self.largo_m, 2),
            "ancho_m": round(self.ancho_m, 2),
            "area_m2": round(area, 2),
            "lux_objetivo": round(self.lux_objetivo, 2),
            "lumenes_aprox": round(area * self.lux_objetivo, 2),
        }


class ParcelaAgricola:
    def __init__(self, hectareas: float, rendimiento_t_ha: float) -> None:
        self.hectareas = float(hectareas)
        self.rendimiento_t_ha = float(rendimiento_t_ha)

    def resumen(self) -> dict:
        produccion = self.hectareas * self.rendimiento_t_ha
        return {
            "hectareas": round(self.hectareas, 4),
            "rendimiento_t_ha": round(self.rendimiento_t_ha, 4),
            "produccion_estimada_t": round(produccion, 3),
        }

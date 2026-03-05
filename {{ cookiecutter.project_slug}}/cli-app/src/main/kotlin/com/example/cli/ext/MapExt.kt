package {{ cookiecutter.group_id }}.ext

import com.fasterxml.jackson.databind.ObjectMapper


fun <K, V> Map<K, V>.toJson(): String {
    return ObjectMapper().writeValueAsString(this)
}
package {{ cookiecutter.group_id }}

import cn.hutool.crypto.SmUtil
import cn.hutool.crypto.asymmetric.KeyType
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.boot.context.properties.ConstructorBinding
import org.springframework.boot.context.properties.EnableConfigurationProperties
import org.springframework.stereotype.Component

@Component
@EnableConfigurationProperties
@ConfigurationProperties("app")
data class AppProperties(
    val properties: List<Property>
) {

    @ConstructorBinding
    data class Property(
        val table: String,
        val name: String,
        val taskId: String,
        val publicKey: String
    ) {
        fun encrypt(data: String): String {

            val sm2 = SmUtil.sm2(null, this.publicKey)

            return sm2.encryptBcd(data, KeyType.PublicKey)
        }
    }
}
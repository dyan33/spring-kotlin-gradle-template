package {{ cookiecutter.group_id }}

import org.slf4j.Logger
import org.slf4j.LoggerFactory
import org.springframework.boot.ApplicationArguments
import org.springframework.boot.ApplicationRunner
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.stereotype.Component


@Component
class APPRunner(
    val jdbcTemplate: JdbcTemplate,
    val appProperties: AppProperties
) : ApplicationRunner {


    val logger: Logger = LoggerFactory.getLogger(APPRunner::class.java)


    override fun run(args: ApplicationArguments?) {
        logger.info("Running APPRunner")
        logger.info("APPRunner properties: ${appProperties.properties}")
    }

}
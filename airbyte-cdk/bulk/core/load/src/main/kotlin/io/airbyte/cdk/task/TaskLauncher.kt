/*
 * Copyright (c) 2024 Airbyte, Inc., all rights reserved.
 */

package io.airbyte.cdk.task

interface Task {
    suspend fun execute()
}

/**
 * A TaskLauncher is responsible for starting and stopping the task workflow, and for managing
 * transitions between tasks.
 */
interface TaskLauncher {
    val taskRunner: TaskRunner

    suspend fun start()
    suspend fun stop() {
        taskRunner.close()
    }
}

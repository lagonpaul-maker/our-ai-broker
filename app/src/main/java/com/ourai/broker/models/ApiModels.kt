package com.ourai.broker.models

data class ChatRequest(
    val message: String,
    val model: String = "ox-alpha"
)

data class ChatResponse(
    val message: String
)

data class StatusResponse(
    val status: String,
    val version: String
)

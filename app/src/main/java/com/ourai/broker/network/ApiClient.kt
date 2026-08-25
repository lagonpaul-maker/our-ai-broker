package com.ourai.broker.network

import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

object ApiClient {
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .build()

    fun sendMessage(
        baseUrl: String,
        userMessage: String,
        callback: (Result<String>) -> Unit
    ) {
        val json = JSONObject().apply {
            put("message", userMessage)
        }

        val mediaType = "application/json; charset=utf-8".toMediaType()
        val body = json.toString().toRequestBody(mediaType)

        val request = Request.Builder()
            .url("$baseUrl/api/chat")
            .post(body)
            .build()

        client.newCall(request).enqueue(object : okhttp3.Callback {
            override fun onFailure(
                call: okhttp3.Call,
                e: java.io.IOException
            ) {
                callback(Result.failure(e))
            }

            override fun onResponse(
                call: okhttp3.Call,
                response: okhttp3.Response
            ) {
                response.use {
                    val responseBody = it.body?.string() ?: ""

                    if (it.isSuccessful) {
                        try {
                            val jsonResponse = JSONObject(responseBody)
                            val reply = jsonResponse.optString(
                                "message",
                                "No response content"
                            )
                            callback(Result.success(reply))
                        } catch (e: Exception) {
                            callback(Result.failure(e))
                        }
                    } else {
                        callback(
                            Result.failure(
                                Exception("Server returned status: ${it.code}")
                            )
                        )
                    }
                }
            }
        })
    }
}

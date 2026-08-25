package com.ourai.broker

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.ourai.broker.network.ApiClient

class MainActivity : AppCompatActivity() {

    private lateinit var tvChatLog: TextView
    private lateinit var etMessage: EditText
    private lateinit var btnSend: Button

    private val baseUrl = "http://127.0.0.1:8080"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tvChatLog = findViewById(R.id.tvChatLog)
        etMessage = findViewById(R.id.etMessage)
        btnSend = findViewById(R.id.btnSend)

        btnSend.setOnClickListener {
            val userText = etMessage.text.toString().trim()

            if (userText.isNotEmpty()) {
                appendChat("You: $userText")
                etMessage.setText("")

                ApiClient.sendMessage(baseUrl, userText) { result ->
                    runOnUiThread {
                        result.onSuccess { response ->
                            appendChat("AI: $response")
                        }.onFailure { error ->
                            appendChat("Error: ${error.localizedMessage}")
                        }
                    }
                }
            }
        }
    }

    private fun appendChat(message: String) {
        val currentText = tvChatLog.text.toString()
        tvChatLog.text = "$currentText\n\n$message"
    }
}

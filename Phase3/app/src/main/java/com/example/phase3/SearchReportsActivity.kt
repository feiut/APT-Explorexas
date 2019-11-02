package com.example.phase3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.ListView
import android.widget.SearchView
import android.widget.TextView
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley

class SearchReportsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search_reports)
//        var mySearchView: SearchView= findViewById(R.id.searchView)
//        var myList: ListView = findViewById(R.id.mySearchList)
//
//        // Instantiate the RequestQueue.
//        val queue = Volley.newRequestQueue(this)
//        val url = "https://apt-team7.appspot.com/"
        // Request a string response from the provided URL.
//        val stringRequest = StringRequest(Request.Method.GET, url,
//            Response.Listener<String> { response ->
//                textView.text = "Response is: ${response.substring(0, 500)}"
//            },
//            Response.ErrorListener { textView.text = "That didn't work!" })

        // Add the request to the RequestQueue.
//        queue.add(stringRequest)
    }
}

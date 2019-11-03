package com.example.phase3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.inputmethod.EditorInfo
import android.widget.ListView
import android.widget.SearchView
import android.widget.TextView
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.StringRequest
import com.android.volley.toolbox.Volley
import kotlinx.android.synthetic.main.activity_create_report.*

class SearchReportsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_search_reports)
        var mySearchView: SearchView= findViewById(R.id.searchView) as SearchView
        var myList: ListView = findViewById(R.id.mySearchList)

        val queue = Volley.newRequestQueue(this)

        mySearchView.setOnQueryTextListener(object : SearchView.OnQueryTextListener{
            override fun onQueryTextChange(newText: String): Boolean {
                return false
            }
            override fun onQueryTextSubmit(query: String): Boolean {
                var url = getString(R.string.website_url)
                url = url + "searchTag/" + query
                val stringRequest = StringRequest(Request.Method.GET, url,
                    Response.Listener {
                            response ->
                        if(response==null){
                            findViewById<TextView>(R.id.search_text).text = "No Matching Tag Found!"
                        }else {
                            findViewById<TextView>(R.id.search_text).text =
                                "Search result is: ${response}"
                        }
                    },
                    Response.ErrorListener { findViewById<TextView>(R.id.search_text).text = "That didn't work!" })
                queue.add(stringRequest)
                return false
            }

        })


    }
}

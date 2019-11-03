package com.example.phase3

import android.content.Intent
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
        val srchView = findViewById<SearchView>(R.id.searchView)
        srchView.setQueryHint("search tag here")
        srchView.setIconifiedByDefault(false)
        srchView.setOnQueryTextListener(object: SearchView.OnQueryTextListener {
            override fun onQueryTextChange(newText: String): Boolean {
                return false
            }

            override fun onQueryTextSubmit(query: String): Boolean {
                val catRptIntent = Intent(this@SearchReportsActivity, CategoryReportActivity::class.java);
                catRptIntent.putExtra("Type", "Search")
                catRptIntent.putExtra("Pattern", query)
                startActivity(catRptIntent)
                return true
            }
        })
    }
}

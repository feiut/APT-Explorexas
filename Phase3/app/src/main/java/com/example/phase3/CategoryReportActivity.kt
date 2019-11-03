package com.example.phase3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.TextView
import android.widget.ImageView
import com.squareup.picasso.Picasso
import android.content.Intent
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.android.volley.Request
import com.android.volley.Response
import com.android.volley.toolbox.*
import org.json.JSONArray
import org.json.JSONObject
import android.view.LayoutInflater
import android.view.ViewGroup
import com.example.phase3.ViewReportActivity.Companion.webUrl


class CategoryReportActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_category_report)

        currActivity = this@CategoryReportActivity
        val type = intent.getStringExtra("Type")
        if (type == "Search") {
            val pattern = intent.getStringExtra("Pattern")!!
            getSearchReport(pattern)
        } else {
                val catId = intent.getStringExtra("cat_id")!!
                getCategoryReport(catId)
        }
    }

    private fun getSearchReport(pattern: String) {
        val queue = Volley.newRequestQueue(this)
        val url: String = webUrl+"searchTag/"+pattern
        val recyclerView: RecyclerView = findViewById(R.id.recyclerView)

        val jsonArrayRequest = JsonArrayRequest(Request.Method.GET, url, null,
            Response.Listener<JSONArray> { response ->
                    if(response.getJSONObject(0).has("title")) {
                        reportContentList = response
                        val reportItemList = mutableListOf<ReportItem>()
                        for (reportIdx in 0 until reportContentList.length()) {
                            val report: JSONObject = reportContentList.getJSONObject(reportIdx)
                            reportItemList.add(
                                ReportItem(
                                    report.getString("title"),
                                    report.getString("imgId")
                                )
                            )
                        }
                        val keyword = "Keyword:  " + pattern
                        findViewById<TextView>(R.id.categoryTextView).text = keyword
                        recyclerView.layoutManager = LinearLayoutManager(this)
                        recyclerView.adapter = Adapter(reportItemList)
                    } else {
                        findViewById<TextView>(R.id.categoryTextView).text = "No Matching Result"
                    }
            },
            Response.ErrorListener { error->
                val nameTextView = findViewById<TextView>(R.id.categoryTextView)
                nameTextView.text = error.toString()
            })
        queue.add(jsonArrayRequest)
    }

    private fun getCategoryReport(catId: String) {
        val queue = Volley.newRequestQueue(this)
        val url: String = webUrl+"viewCategoryPost/" + catId
        val recyclerView: RecyclerView = findViewById(R.id.recyclerView)

        val jsonArrayRequest = JsonArrayRequest(Request.Method.GET, url, null,
            Response.Listener<JSONArray> { response ->
                reportContentList = response
                val reportItemList = mutableListOf<ReportItem>()
                for(reportIdx in 0 until reportContentList.length()) {
                    val report: JSONObject = reportContentList.getJSONObject(reportIdx)
                    reportItemList.add(ReportItem(report.getString("title"), report.getString("imgId")))
                }
                val catName = "Category:"+ reportContentList.getJSONObject(0).getString("categoryName")
                findViewById<TextView>(R.id.categoryTextView).text =  catName
                recyclerView.layoutManager = LinearLayoutManager(this)
                recyclerView.adapter = Adapter(reportItemList)
            },
            Response.ErrorListener { error->
                val nameTextView = findViewById<TextView>(R.id.categoryTextView)
                nameTextView.text = error.toString()
            })
        queue.add(jsonArrayRequest)
    }

    companion object {
        //var cat_id:String = "Other"
        //var webUrl:String = "http://explore-texas-web.appspot.com/"
        var webUrl:String = "http://apt-team7.appspot.com/"
        lateinit var currActivity: AppCompatActivity
        lateinit var reportContentList:JSONArray
    }
}

private class ReportItem(_title: String, _imgId: String) {
    val title = _title
    val imgId = _imgId
}

private class Adapter(val reports: List<ReportItem>) : RecyclerView.Adapter<Adapter.ViewHolder>() {
    override fun getItemCount() = reports.size

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val itemView = LayoutInflater.from(parent.context).inflate(R.layout.report_item_layout, parent, false)
        return ViewHolder(itemView)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val imgUrl: String = CategoryReportActivity.webUrl + "images/" + reports[position].imgId
        holder.textView.text = reports[position].title
        Picasso.get().load(imgUrl).into(holder.imgView)

        holder.textView.setOnClickListener(object: View.OnClickListener {
            override fun onClick(v : View?) {
                val viewRptIntent = Intent(CategoryReportActivity.currActivity, ViewReportActivity::class.java)
                viewRptIntent.putExtra(ViewReportActivity.report, CategoryReportActivity.reportContentList.getJSONObject(position).toString())
                CategoryReportActivity.currActivity.startActivity(viewRptIntent)
            }
        })
    }

    class ViewHolder(itemView: View): RecyclerView.ViewHolder(itemView) {
        var textView = itemView.findViewById<TextView>(R.id.titleTextViewListItem)!!
        var imgView = itemView.findViewById<ImageView>(R.id.imageViewListItem)!!
    }
}
package com.example.phase3

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.TextView
import android.widget.ImageView
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.activity_view_report.*
import org.json.JSONObject

class ViewReportActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_view_report)

        val reportContent: String? = intent.getStringExtra(report)
        val reportJson = JSONObject(reportContent!!)
        val imgString = reportJson.getString("imgId")
        val imgUrl = webUrl + "images/" + imgString
        val imgView = findViewById<ImageView>(R.id.reportImageView)
        Picasso.get().load(imgUrl).into(imgView)
        findViewById<TextView>(R.id.reportTextViewUser).text = reportJson.getString("userName")
        findViewById<TextView>(R.id.reportTextViewPlace).text = reportJson.getString("placeName")
        findViewById<TextView>(R.id.reportTextViewReview).text = reportJson.getString("review")
        findViewById<TextView>(R.id.reportTextViewRating).text = reportJson.getString("rating")
        findViewById<TextView>(R.id.reportTextViewTime).text = reportJson.getString("timeStamp")
        findViewById<TextView>(R.id.reportTextViewCategory).text = reportJson.getString("categoryName")
        findViewById<TextView>(R.id.reportTextViewTitle).text = reportJson.getString("title")
        findViewById<TextView>(R.id.reportTextViewTag).text = "#"+reportJson.getString("tag")
    }

    companion object {
        var report: String = ""
        val webUrl: String = "http://explore-texas-web.appspot.com/"
        //var webUrl:String = "http://apt-team7.appspot.com/"
    }
}

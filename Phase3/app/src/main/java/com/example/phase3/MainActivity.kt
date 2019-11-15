package com.example.phase3
//import android.content.Intent
//import android.graphics.Bitmap
//import android.provider.MediaStore
//import android.widget.Button
//import android.widget.ImageView
//import kotlinx.android.synthetic.main.activity_take_photo.*
//import androidx.core.app.ComponentActivity.ExtraData
//import androidx.core.content.ContextCompat.getSystemService
//import android.icu.lang.UCharacter.GraphemeClusterBreak.T
//import sun.jvm.hotspot.utilities.IntArray
import android.content.Context
import android.content.Intent
import android.opengl.Visibility
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.FragmentActivity
import android.widget.ImageView
import kotlinx.android.synthetic.main.activity_take_photo.*
import androidx.core.app.ComponentActivity.ExtraData
import androidx.core.content.ContextCompat.getSystemService
import android.icu.lang.UCharacter.GraphemeClusterBreak.T
import android.widget.SearchView
import android.widget.TextView
//import com.example.phase3.MenuActivity.Companion.getLaunchIntent
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.SignInButton
import com.google.android.gms.common.api.ApiException
import com.google.android.gms.tasks.OnCompleteListener
import com.google.android.gms.tasks.Task
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_main.welcome_title
import kotlinx.android.synthetic.main.activity_menu.*

//import androidx.core.app.ActivityCompat.startActivityForResult
//import androidx.core.app.ComponentActivity.ExtraData
//import androidx.core.content.ContextCompat.getSystemService
//import android.icu.lang.UCharacter.GraphemeClusterBreak.T
//import sun.jvm.hotspot.utilities.IntArray

class MainActivity : AppCompatActivity() {

    val RC_SIGN_IN: Int = 1
    lateinit var mGoogleSignInClient: GoogleSignInClient

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Sign in
        val gso : GoogleSignInOptions = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestEmail()
            .build()
        mGoogleSignInClient = GoogleSignIn.getClient(this, gso)
        sign_in_button.visibility=View.VISIBLE
        sign_in_button.setSize(SignInButton.SIZE_STANDARD)
        sign_in_button.setOnClickListener {
            val signInIntent = mGoogleSignInClient.getSignInIntent()
            startActivityForResult(signInIntent, RC_SIGN_IN)
        }
    }

    fun signOut(){
        mGoogleSignInClient.signOut()
            .addOnCompleteListener(this, object:OnCompleteListener<Void>{
                override fun onComplete(p0: Task<Void>) {
                    FirebaseAuth.getInstance().signOut()
//                    sign_in_button.visibility=View.VISIBLE
//                    layout_buttons.visibility=View.GONE
                }
            })
//        startActivity(getLaunchIntent(this))
    }
    companion object {
        fun getLaunchIntent(from: Context) = Intent(from, MainActivity::class.java).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        Log.d("debug", requestCode.toString() + " vs " + RC_SIGN_IN.toString() + ", compare:" + (requestCode == RC_SIGN_IN).toString())
        if (requestCode == RC_SIGN_IN) {
            val task :Task<GoogleSignInAccount> = GoogleSignIn.getSignedInAccountFromIntent(data)
            handleSignInResult(task)
        }
    }

    private fun handleSignInResult(completedTask : Task<GoogleSignInAccount>){
        try{
            sign_in_button.visibility=View.GONE
            val account:GoogleSignInAccount? = completedTask.getResult(ApiException::class.java)
            val viewMenuIntent = Intent(this, MenuActivity::class.java)
            viewMenuIntent.putExtra("clientAccount", account!!.displayName)
            viewMenuIntent.putExtra("clientAccountEmail",account!!.email)
            signOut()
            startActivity(viewMenuIntent)
        } catch (e:ApiException){
            Log.d("exception","Login failed due to:" + e.message)
        }
    }
}

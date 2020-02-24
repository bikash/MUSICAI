ersion "2.18.2"
    \header { 
    tagline = ""  % removed 
    } 
#(set-global-staff-size 20)

\score {
  {
    \repeat unfold 2 { s1 \break }
  }
  \layout {
    indent = 0\in
    \context {
      \Staff
      \remove "Time_signature_engraver"
      \remove "Clef_engraver"
      \remove "Bar_engraver"
    }
    \context {
      \Score
      \remove "Bar_number_engraver"
    }
  }
}

